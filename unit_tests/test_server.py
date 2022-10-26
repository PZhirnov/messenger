import sys
import os
import unittest
from server.core import MessageProcessor

sys.path.insert(0, os.path.join(os.getcwd(), '..'))

from common.variables import ACTION, ACCOUNT_NAME, RESPONSE, PRESENCE, ERROR, TIME, USER


class TestServer(unittest.TestCase):
    """
    Тестрирование сервера - ф-ия process_client_msg
    """
    ok_dict = {
        RESPONSE: 200,
    }

    err_dict = {
        RESPONSE: 400,
        ERROR: 'Bad request'
    }

    def test_ok_check(self):
        """
        Проверяется корректный запрос - ответ должен быть 200
        """
        self.assertEqual(
            MessageProcessor.process_message(
                {ACTION: PRESENCE, TIME: 1.1, USER: {ACCOUNT_NAME: 'Guest'}}
            ), self.ok_dict
        )

    def test_no_action(self):
        """
        Действие не указано
        """
        self.assertEqual(
            MessageProcessor.process_message(
                {TIME: 1.1, USER: {ACCOUNT_NAME: 'Guest'}}
            ), self.err_dict
        )

    def test_no_time(self):
        """
        Действие не указано
        """
        self.assertEqual(
            MessageProcessor.process_message(
                {ACTION: PRESENCE, USER: {ACCOUNT_NAME: 'Guest'}}
            ), self.err_dict
        )

    def test_wrong_action(self):
        """
        Действие не указано
        """
        self.assertEqual(
            MessageProcessor.process_message(
                {ACTION: 'no action', TIME: 1.1, USER: {ACCOUNT_NAME: 'Guest'}}
            ), self.err_dict
        )

    def test_account_name(self):
        """
        Проверка имени пользователя
        """
        self.assertEqual(
            MessageProcessor.process_message(
                {ACTION: PRESENCE, TIME: 1.1, USER: {ACCOUNT_NAME: 'Bad name'}}
            ), self.err_dict
        )

    def test_response_dict(self):
        """
        Проверка того, что фнкция возвращает словарь - при 200 и 400
        """
        # assertNotEqual
        self.assertIsInstance(
            MessageProcessor.process_message(
                {ACTION: PRESENCE, TIME: 1.1, USER: {ACCOUNT_NAME: 'Guest'}}
            ), dict
        )
        self.assertIsInstance(
            MessageProcessor.process_message(
                {ACTION: PRESENCE, }
            ), dict
        )

    def test_response_empty_param(self):
        """
        Проверка случая, когда в функцию не был передан параметр
        """
        with self.assertRaises(TypeError):
            MessageProcessor.process_message()


if __name__ == '__main__':
    unittest.main()
