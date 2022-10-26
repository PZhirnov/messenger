import os
import sys
import unittest
import json
from common.utils import get_message, send_message
from common.variables import RESPONSE, ERROR, USER, ACCOUNT_NAME, TIME, ACTION, PRESENCE, ENCODING

sys.path.insert(0, os.path.join(os.getcwd(), '..'))
print(sys.path)


class TestSocket:
    """Класс осуществляет имитацию работы сокета"""

    def __init__(self, test_dict):
        self.test_dict = test_dict
        self.encoded_message = None
        self.received_message = None

    def send(self, message_to_send):
        """Функция отправляет сообщение.
        :param message_to_send: отправляемое сообщение в сокет
        """
        json_test_message = json.dumps(self.test_dict)
        # кодируем сообщение
        self.encoded_message = json_test_message.encode(ENCODING)
        # данные, которые будут отправлены в сокет
        self.received_message = message_to_send

    def recv(self, max_len):
        """Получаем данные из сокета
        :param max_len: длина сообщения в байтах (не обязательный)
        :return: данные в формате json
        """
        json_test_message = json.dumps(self.test_dict)
        return json_test_message.encode(ENCODING)


class TestUtils(unittest.TestCase):
    """Класс, выполняющий тестирование отправку и получение ответов."""
    test_dict_send = {
        ACTION: PRESENCE,
        TIME: 111111.111111,
        USER: {
            ACCOUNT_NAME: 'test_test'
        }
    }
    test_dict_recv_ok = {RESPONSE: 200}
    test_dict_recv_err = {
        RESPONSE: 400,
        ERROR: 'Bad Request'
    }

    def test_send_message_true(self):
        """Тестрирование корректности функции отправки
        :return:
        """
        # создаем экземпляр тестового словаря
        test_socket = TestSocket(self.test_dict_send)
        # вызов тестирующей функции
        send_message(test_socket, self.test_dict_send)
        self.assertEqual(test_socket.encoded_message, test_socket.received_message)

    def test_send_message_with_error(self):
        # экземпля тестового словаря
        test_socket = TestSocket(self.test_dict_send)
        # вызов тестируемой функции
        send_message(test_socket, self.test_dict_send)
        self.assertRaises(TypeError, send_message, test_socket, "wrong_dictionary")

    def test_get_message_ok(self):
        """Тестирование функции приема сообщения"""
        test_sock_ok = TestSocket(self.test_dict_recv_ok)
        self.assertEqual(get_message(test_sock_ok), self.test_dict_recv_ok)

    def test_get_message_error(self):
        """Тестирование функции приема сообщения с ошибкой"""
        test_sock_err = TestSocket(self.test_dict_recv_err)
        self.assertEqual(get_message(test_sock_err), self.test_dict_recv_err)


if __name__ == '__main__':
    unittest.main()
