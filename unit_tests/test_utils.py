import os
import sys
import unittest
import json

sys.path.insert(0, os.path.join(os.getcwd(), '..'))

from common.variables import RESPONSE, ERROR, USER, ACCOUNT_NAME, TIME, ACTION, PRESENCE, ENCODING
from common.utils import get_message, send_message


class TestSocket:
    """
    Класс используется для тестирования отправки и получения сообщения.
    При инициализации принимает словарь с данными.
    """

    def __init__(self, test_dict):
        self.test_dict = test_dict
        self.encoded_message = None
        self.received_message = None

    def send(self, message_to_send):
        """
        Функция отправляет сообщение.
        :param message_to_send: отправляемое сообщение в сокет
        :return:
        """
        json_test_message = json.dumps(self.test_dict)
