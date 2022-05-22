""" Клиент """

import socket
import sys
import json
import time
from common.variables import *
from common.utils import get_message, send_message


def create_presence(account_name='Guest12'):
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
    return out_data


def process_ans(msg):
    """
    Функция для анализа ответа сервера
    :param msg: переданный словарь
    :return:
    """
    if RESPONSE in msg:
        if msg[RESPONSE] == 200:
            return '200 : OK'
        return f'400 : {msg[ERROR]}'
    raise ValueError


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
        server_address = DEFAULT_IP_address
        server_port = DEFAULT_PORT
    except ValueError:
        print('Порт должен быть указан из диапазона от 1024 до 65535.')
        sys.exit(1)

    # Создание сокета и обмен
    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.connect((server_address, server_port))
    msg_to_server = create_presence()
    send_message(transport, msg_to_server)

    try:
        answer = process_ans(get_message(transport))
        print(answer)
    except (ValueError, json.JSONDecodeError):
        print('Сообщение сервера не удалось декодировать')


if __name__ == '__main__':
    main()
