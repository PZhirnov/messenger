""" Клиент"""
import socket
import sys
import json
import time
import logging
import logs.client_log_config
from common.variables import *
from common.utils import get_message, send_message
from errors import ReqFieldMissingError, IncorrectDataRecivedError, NonDictInputError

# Инициализация клиентского логера
CLIENT_LOGGER = logging.getLogger('client')


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


def main():
    """
    Функция считывает переданные аргументы, настраивает сокет и отправляет ответ
    """
    try:
        server_address = sys.argv[1]
        server_port = int(sys.argv[2])
        if server_port < 1024 or server_port > 65535:
            raise ValueError
    except IndexError:
        CLIENT_LOGGER.info('Параметры сервера не переданы, запуск'
                           'выполняется с применением значений по умолчанию.'
                           )
        server_address = DEFAULT_IP_address
        server_port = DEFAULT_PORT
    except ValueError:
        CLIENT_LOGGER.error(f'Попытка запуска клиента с недопустимым номером порта: {server_port}.'
                            f'(должно быть значение от 1024 до 65535)')
        # print('Порт должен быть указан из диапазона от 1024 до 65535.')
        sys.exit(1)

    # Инициализация сокета и обмен
    try:
        transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transport.connect((server_address, server_port))
        CLIENT_LOGGER.info(f'Уданое подключение к серверу {server_address}:{server_port}')
        msg_to_server = create_presence()
        send_message(transport, msg_to_server)
        answer = process_ans(get_message(transport))
        transport.close()
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


if __name__ == '__main__':
    main()
