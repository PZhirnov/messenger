"""
Сервер
"""
import sys
import json
import socket
import logging
import logs.server_log_config
from common.variables import *
from common.utils import get_message, send_message
from errors import IncorrectDataRecivedError, ReqFieldMissingError, NonDictInputError

# Инициализация серверного логера
SERVER_LOGGER = logging.getLogger('server')


def process_client_msg(msg):
    """
    Функция обрабатывает сообщения от клиентов,
    проверяет корректность данных и возвращает словарь для ответа клиенту
    :param msg: словарь
    :return: ответ в виде словаря для клиента
    """
    try:
        # Проверка на наличие словаря в переменной msg
        if not isinstance(msg, dict):
            raise NonDictInputError

        conditions = ACTION in msg and msg[ACTION] == PRESENCE \
                     and TIME in msg and USER in msg \
                     and msg[USER][ACCOUNT_NAME] == 'Guest'
        # Если True, то отдаем 200 код.
        if conditions:
            return {RESPONSE: 200}
        return {
            RESPONSE: 400,
            ERROR: 'Bad request',
        }
    except NonDictInputError as err:
        SERVER_LOGGER.error(err)


def main():
    """
    Функция загружает параметры командной строки и запускает сервер
    Формат команды: server.py -p 8888 -a 127.0.0.1
    :return:
    """
    print('сработал')
    # Получаем порт или устанаваливаем значение по умолчанию
    try:
        if '-p' in sys.argv:
            listen_port = int(sys.argv[sys.argv.index('-p') + 1])
        else:
            listen_port = DEFAULT_PORT
        if listen_port < 1024 or listen_port > 65535:
            raise ValueError
    except IndexError:
        SERVER_LOGGER.error('Не указан номер порта после параметра - \'p\'! '
                            'Сервер не будет запущен!')
        # print('Вы не указали номер порта после параметра - \'p\'!')
    except ValueError:
        SERVER_LOGGER.error(f'Попытка запуска сервера с недопустимым номером порта: {listen_port}.'
                            f'(должно быть значение от 1024 до 65535)')

    # Получаем ip или устанаваливаем значение по умолчанию
    try:
        if '-a' in sys.argv:
            listen_ip = sys.argv[sys.argv.index('-a') + 1]
        else:
            listen_ip = ''
    except IndexError:
        SERVER_LOGGER.error('После параметра \'-a\' не указан ip адрес. '
                            'Сервер не будет запущен.')

    # Готовим сокет
    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    transport.bind((listen_ip, listen_port))

    # Слушаем порт
    transport.listen(MAX_CONNECTIONS)
    SERVER_LOGGER.info('Сервер запущен и находится в режиме ожидания.')

    while True:
        client, client_address = transport.accept()
        try:
            # Получаем сообщение от клиента из функции, созданной в utils
            msg_from_client = get_message(client)
            account_name_client = msg_from_client["user"]["account_name"]  # получим имя клиента из сообщения
            print(msg_from_client)
            # Готовим ответ клиенту
            response = process_client_msg(msg_from_client)
            # Отправляем ответ клиенту и закрываем сокет
            send_message(client, response)
            SERVER_LOGGER.info(f'Отправлен ответ клиенту {account_name_client}.')
            client.close()
        except json.JSONDecodeError:
            SERVER_LOGGER.error(f'Не удалось декодировать json строку, полученную'
                                f' от клиента {account_name_client} - {client_address}!')
            # print('Принято некорректное собщение от клиента!')
            client.close()
        except IncorrectDataRecivedError:
            SERVER_LOGGER.error(f'От клиента {client_address} приняты некорректные данные.'
                                f'Соедниение будет закрыто.')
            client.close()


if __name__ == '__main__':
    main()
