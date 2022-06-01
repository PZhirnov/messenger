"""
------ Утилиты приложения ------
"""

import json
from common.variables import MAX_PACKAGE_LENGTH, ENCODING
from decos import log


@log
def get_message(client):
    """
    Функция принимает и декодирует сообщения
    :param client: клиентский сокет (содержит данные из переданного сообщения в байтах
    :return: словарь
    """
    # Принимаем сообщение в байтах
    encoded_response = client.recv(MAX_PACKAGE_LENGTH)
    # Проводим валидацию данных и если все ок, то возвращаем словарь
    if isinstance(encoded_response, bytes):
        json_response = encoded_response.decode(ENCODING)
        if isinstance(json_response, str):
            response = json.loads(json_response)  # из строки получаем словарь
            if isinstance(response, dict):
                return response  # возвращаем словарь
            raise ValueError
        raise ValueError
    raise ValueError


@log
def send_message(sock, message):
    """
    Утилита кодирования и отправки сообещния:
    1. Принимает словарь для отправки
    2. Преобразует в байты и отправляет
    :param sock: переданный в функцию сокет
    :param message: словарь с данными для отправки
    """

    if not isinstance(message, dict):
        raise TypeError
    js_message = json.dumps(message)
    encoded_message = js_message.encode(ENCODING)
    sock.send(encoded_message)


