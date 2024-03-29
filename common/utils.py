"""
------ Утилиты приложения ------
"""

import json
from common.variables import MAX_PACKAGE_LENGTH, ENCODING
from common.decos import log
import sys
sys.path.append('../')


@log
def get_message(client):
    """
    Утилита приёма и декодирования сообщения принимает байты выдаёт словарь,
    если приняточто-то другое отдаёт ошибку значения
    :param client:
    :return:
    """
    encoded_response = client.recv(MAX_PACKAGE_LENGTH)
    json_response = encoded_response.decode(ENCODING)
    response = json.loads(json_response)
    if isinstance(response, dict):
        return response
    else:
        raise TypeError


@log
def send_message(sock, message):
    """
    Утилита кодирования и отправки сообещния:
    1. Принимает словарь для отправки
    2. Преобразует в байты и отправляет
    :param sock: переданный в функцию сокет
    :param message: словарь с данными для отправки
    """
    js_message = json.dumps(message)
    encoded_message = js_message.encode(ENCODING)
    sock.send(encoded_message)
