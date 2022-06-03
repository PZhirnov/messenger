"""
Сервер
"""
import select
import sys
import json
import socket
import logging
import logs.server_log_config
from common.variables import *
from common.utils import get_message, send_message
from errors import IncorrectDataRecivedError, ReqFieldMissingError, NonDictInputError
from decos import log
import argparse
import time

# Инициализация серверного логера
SERVER_LOGGER = logging.getLogger('server')


@log
def process_client_msg(msg, msg_list, client):
    """
    Обработчик сообщений от клиентов
    :param msg: словарь
    :param msg_list: список сообщений
    :param client:
    :return:
    """
    try:
        # Проверка на наличие словаря в переменной msg
        if not isinstance(msg, dict):
            raise NonDictInputError

        conditions = ACTION in msg and msg[ACTION] == PRESENCE \
                     and TIME in msg and USER in msg \
                     and msg[USER][ACCOUNT_NAME] == 'Guest'
        # Если передано сообщение
        msg_in_deque = ACTION in msg and msg[ACTION] == MESSAGE and \
                       TIME in msg and MESSAGE_TEXT in msg
        # Если True, то отдаем 200 код.
        if conditions:
            send_message(client, {RESPONSE: 200})
            return
        elif msg_in_deque:
            # Если передано сообщение, то оно добавляется в очередь
            msg_list.append((msg[ACCOUNT_NAME], msg[MESSAGE_TEXT]))
            return
        else:
            send_message(client, {RESPONSE: 400, ERROR: 'Bad request'})
            return
    except NonDictInputError as err:
        SERVER_LOGGER.error(err)


@log
def arg_parser():
    """Парсер аргументов коммандной строки"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', default=DEFAULT_PORT, type=int, nargs='?')
    parser.add_argument('-a', default='', nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    listen_address = namespace.a
    listen_port = namespace.p

    # проверка получения корретного номера порта для работы сервера.
    if not 1023 < listen_port < 65536:
        LOGGER.critical(
            f'Попытка запуска сервера с указанием неподходящего порта '
            f'{listen_port}. Допустимы адреса с 1024 до 65535.')
        sys.exit(1)

    return listen_address, listen_port


def main():
    """
    Функция загружает параметры командной строки и запускает сервер
    Формат команды: server.py -p 8888 -a 127.0.0.1
    :return:
    """
    # Загрузка параметров командной строки
    listen_ip, listen_port = arg_parser()

    # Готовим сокет
    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # transport.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    transport.bind((listen_ip, listen_port))
    transport.settimeout(0.5)

    # Список клиентов и очередь сообщений
    clients = []
    messages = []

    # Слушаем порт
    transport.listen(MAX_CONNECTIONS)
    SERVER_LOGGER.info('Сервер запущен и находится в режиме ожидания.')

    while True:
        # Ждём подключение
        try:
            client, client_address = transport.accept()
        except OSError as err:
            print(err.errno)  # The error number returns None because it's just a timeout
            pass
        else:
            SERVER_LOGGER.info(f'Установлено соедение с ПК {client_address}')
            clients.append(client)

        recv_data_lst = []
        send_data_lst = []
        err_lst = []
        # Проверяем наличие ждущих клиентов
        try:
            if clients:
                recv_data_lst, send_data_lst, err_lst = select.select(clients, clients, [], 0)
        except OSError:
            pass

        # принимаем сообщения и если там есть сообщения,
        # кладём в словарь, если ошибка, исключаем клиента.
        if recv_data_lst:
            for client_with_message in recv_data_lst:
                try:
                    process_client_msg(get_message(client_with_message), messages, client_with_message)
                except:
                    SERVER_LOGGER.info(f'Клиент {client_with_message.getpeername()} '
                                f'отключился от сервера.')
                    clients.remove(client_with_message)

        # Если есть сообщения для отправки и ожидающие клиенты, отправляем им сообщение.
        if messages and send_data_lst:
            message = {
                ACTION: MESSAGE,
                SENDER: messages[0][0],
                TIME: time.time(),
                MESSAGE_TEXT: messages[0][1]
            }
            del messages[0]
            for waiting_client in send_data_lst:
                try:
                    send_message(waiting_client, message)
                except:
                    SERVER_LOGGER.info(f'Клиент {waiting_client.getpeername()} отключился от сервера.')
                    waiting_client.close()
                    clients.remove(waiting_client)


if __name__ == '__main__':
    main()
