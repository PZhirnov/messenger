""" Клиент"""
import socket
import sys
import json
import time
import logging
import argparse
import logs.client_log_config
from common.variables import *
from common.utils import get_message, send_message
from errors import ReqFieldMissingError, IncorrectDataRecivedError, NonDictInputError
from decos import log

# Инициализация клиентского логера
CLIENT_LOGGER = logging.getLogger('client')


@log
def message_from_server(message):
    """Функция - обработчик сообщений других пользователей, поступающих с сервера"""
    if ACTION in message and message[ACTION] == MESSAGE and \
            SENDER in message and MESSAGE_TEXT in message:
        print(f'Получено сообщение от пользователя '
              f'{message[SENDER]}:\n{message[MESSAGE_TEXT]}')
        CLIENT_LOGGER.info(f'Получено сообщение от пользователя '
                           f'{message[SENDER]}:\n{message[MESSAGE_TEXT]}')
    else:
        CLIENT_LOGGER.error(f'Получено некорректное сообщение с сервера: {message}')


@log
def create_message(sock, account_name='Guest'):
    """Функция запрашивает текст сообщения и возвращает его.
    Так же завершает работу при вводе подобной комманды
    """
    message = input('Введите сообщение для отправки или \'!!!\' для завершения работы: ')
    if message == '!!!':
        sock.close()
        CLIENT_LOGGER.info('Завершение работы по команде пользователя.')
        print('Спасибо за использование нашего сервиса!')
        sys.exit(0)
    message_dict = {
        ACTION: MESSAGE,
        TIME: time.time(),
        ACCOUNT_NAME: account_name,
        MESSAGE_TEXT: message
    }
    CLIENT_LOGGER.debug(f'Сформирован словарь сообщения: {message_dict}')
    return message_dict


@log
def create_presence(account_name='Guest'):
    """
    Функция генерирует запрос о присуствии клиента
    :param account_name: уникальное имя аккаунта или Guest
    :return: словарь с данными запроса
    """
    out_data = {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name
        }
    }
    CLIENT_LOGGER.info(f'Сгенерирован запрос о присутствии клиента {account_name}.')
    return out_data


@log
def process_ans(msg):
    """
    Функция для анализа ответа сервера
    :param msg: переданный словарь
    :return:
    """
    try:
        # Проверка на наличие словаря в переменной msg
        if not isinstance(msg, dict):
            raise NonDictInputError

        if RESPONSE in msg:
            if msg[RESPONSE] == 200:
                return '200 : OK'
            return f'400 : {msg[ERROR]}'
    except NonDictInputError as err:
        CLIENT_LOGGER.error(err)


@log
def arg_parser():
    """Создаём парсер аргументов коммандной строки
    и читаем параметры, возвращаем 3 параметра
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('addr', default=DEFAULT_IP_ADDRESS, nargs='?')
    parser.add_argument('port', default=DEFAULT_PORT, type=int, nargs='?')
    parser.add_argument('-m', '--mode', default='listen', nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    server_address = namespace.addr
    server_port = namespace.port
    client_mode = namespace.mode

    # проверим подходящий номер порта
    if not 1023 < server_port < 65536:
        CLIENT_LOGGER.critical(
            f'Попытка запуска клиента с неподходящим номером порта: {server_port}. '
            f'Допустимы адреса с 1024 до 65535. Клиент завершается.')
        sys.exit(1)

    # Проверим допустим ли выбранный режим работы клиента
    if client_mode not in ('listen', 'send'):
        CLIENT_LOGGER.critical(f'Указан недопустимый режим работы {client_mode}, '
                               f'допустимые режимы: listen , send')
        sys.exit(1)

    return server_address, server_port, client_mode


def main():
    """
    Функция считывает переданные аргументы, настраивает сокет и отправляет ответ
    """
    # Загружаем параметры командной строки
    server_address, server_port, client_mode = arg_parser()
    CLIENT_LOGGER.info(f'Запущен клиент с парамертами: адрес сервера: {server_address}, '
                       f'порт: {server_port}, режим работы: {client_mode}')
    # Инициализация сокета и обмен
    try:
        transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transport.connect((server_address, server_port))
        CLIENT_LOGGER.info(f'Удачное подключение к серверу {server_address}:{server_port}')
        msg_to_server = create_presence()
        send_message(transport, msg_to_server)
        answer = process_ans(get_message(transport))
        # transport.close()
        CLIENT_LOGGER.info(f'Принят ответ от сервера {answer}')
        print(answer)
    except json.JSONDecodeError:
        CLIENT_LOGGER.error('Не удалось декодировать полученную Json строку')
    except ConnectionRefusedError:
        CLIENT_LOGGER.critical(f'Не удалось подключиться к серверу {server_address}:{server_port},'
                               f'конечный компьютер отверг запрос на подключение')
    except ReqFieldMissingError as missing_err:
        CLIENT_LOGGER.error(f'В ответе сервера отсуствует необходимое поле'
                            f'{missing_err.missing_field}')
    else:
        # Если соединение с сервером установлено корректно, начинаем обмен с ним, согласно требуемому режиму.
        # основной цикл прогрммы:
        if client_mode == 'send':
            print('Режим работы - отправка сообщений.')
        else:
            print('Режим работы - приём сообщений.')
        while True:
            # режим работы - отправка сообщений
            if client_mode == 'send':
                try:
                    send_message(transport, create_message(transport))
                except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                    CLIENT_LOGGER.error(f'Соединение с сервером {server_address} было потеряно.')
                    sys.exit(1)

            # Режим работы приём:
            if client_mode == 'listen':
                try:
                    message_from_server(get_message(transport))
                except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                    CLIENT_LOGGER.error(f'Соединение с сервером {server_address} было потеряно.')
                    sys.exit(1)


if __name__ == '__main__':
    main()
