import unittest
import os
import sys
from client import create_presence
from client import process_ans
sys.path.insert(0, os.path.join(os.getcwd(), '..'))

from common.variables import ACTION, TIME, USER, ACCOUNT_NAME, PRESENCE, RESPONSE, ERROR


class TestClient(unittest.TestCase):

    def test_def_presence(self):
        test = create_presence()
        test[TIME] = 1.1
        self.assertEqual(test, {ACTION: PRESENCE, TIME: 1.1, USER: {ACCOUNT_NAME: 'Guest'}})

    def test_presence_no_action(self):
        test = create_presence()
        test[TIME] = 1.1
        self.assertNotEqual(test, {ACTION: 'no action', TIME: 1.1, USER: {ACCOUNT_NAME: 'Guest'}})

    def test_presence_dict(self):
        # Проверка типа возвращаемых данных - должны быть словари
        test = create_presence()
        self.assertIsInstance(test, dict)
        self.assertIsInstance(test[USER], dict)

    def test_presence_account_name(self):
        # Проверка наличие ключа ACCOUNT_NAME
        test = create_presence()
        self.assertTrue(test.get(USER).get(ACCOUNT_NAME))

    def test_presence_with_acoount_name(self):
        # Проверка работоспособности функции с параметром
        user_name = 'test'
        test = create_presence(account_name=user_name)
        self.assertEqual(test.get(USER).get(ACCOUNT_NAME), user_name)

    def test_time_type(self):
        # Проверка типа данные в TIME - должен быть float для time()
        test = create_presence()
        self.assertIsInstance(test[TIME], float)

    def test_200_ans(self):
        self.assertEqual(process_ans({RESPONSE: 200}), '200 : OK')

    def test_400_ans(self):
        self.assertEqual(process_ans({RESPONSE: 400, ERROR: 'Bad Request'}), '400 : Bad Request')

    def test_no_response(self):
        self.assertRaises(ValueError, process_ans, {ERROR: 'Bad Request'})


if __name__ == '__main__':
    unittest.main()
