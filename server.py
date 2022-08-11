"""
Сервер
"""
import select
import sys
import socket
import logging
# import logs.server_log_config
import threading

from common.variables import *
from common.utils import get_message, send_message
# from errors import IncorrectDataRecivedError, ReqFieldMissingError, NonDictInputError
from decos import log
import argparse
from descriptors import Port
from metaclasses import ServerMaker
from server_database import ServerStorage

# Инициализация серверного логгера
SERVER_LOGGER = logging.getLogger('server')


# парсер аргументов командной строки
@log
def arg_parser():
    """Парсер аргументов коммандной строки"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', default=DEFAULT_PORT, type=int, nargs='?')
    parser.add_argument('-a', default='', nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    listen_address = namespace.a
    listen_port = namespace.p
    return listen_address, listen_port


# Класс сервера
class Server(threading.Thread, metaclass=ServerMaker):
    port = Port()

    def __init__(self, listen_address, listen_port, database):
        # 1. Параметры подключения
        self.addr = listen_address
        self.port = listen_port

        # 2. Список подключенных клиентов
        self.clients = []

        # 3. Список сообщение на отправку
        self.messages = []

        # 4. Словарь, содержащий сопоставленные имена и соотвествующие им сокеты
        self.names = dict()

        # 5. База данных сервера
        self.database = database

        # 6. Сокет пустой при запуске
        self.sock = None

        # Конструктор предка
        super().__init__()

    def init_socket(self):
        """
            Функция инициализирует сокет
        """
        # Сохраняем событие в лог
        SERVER_LOGGER.info(
            f'Запущен сервер, порт для подключений: {self.port}, '
            f'адрес с которого принимаются подключения: {self.addr}. '
            f'Если адрес не указан, принимаются соединения с любых адресов.')
        # Выполняем подготовку сокета
        transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transport.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        transport.bind((self.addr, self.port))
        transport.settimeout(0.5)
        # Слушаем сокет
        self.sock = transport
        self.sock.listen()

    def run(self):
        # Выполняем инициализацию сокета
        self.init_socket()

        # Основной цикл программы
        while True:
            # Ждём подключение
            try:
                client, client_address = self.sock.accept()
            except OSError as err:
                # print(err.errno)  # The error number returns None because it's just a timeout
                pass
            else:
                SERVER_LOGGER.info(f'Установлено соедение с ПК {client_address}')
                print(f'Установлено соедение с ПК {client_address}')
                self.clients.append(client)

            recv_data_lst = []
            send_data_lst = []
            err_lst = []
            # Проверяем наличие ждущих клиентов
            # print('клиенты: ', self.clients)
            try:
                if self.clients:
                    recv_data_lst, send_data_lst, err_lst = select.select(self.clients, self.clients, [], 0)
            except OSError:
                pass

            # принимаем сообщения и если там есть сообщения,
            # кладём в словарь, если ошибка, исключаем клиента.
            if recv_data_lst:
                for client_with_message in recv_data_lst:
                    print('клиент', client_with_message)
                    try:
                        self.process_client_msg(get_message(client_with_message), client_with_message)
                    except:
                        SERVER_LOGGER.info(f'Клиент {client_with_message.getpeername()} '
                                           f'отключился от сервера.')
                        self.clients.remove(client_with_message)

            # Если есть сообщения, то обрабатываем каждое
            for msg in self.messages:
                try:
                    # print('Вызов self.process_message: ', msg)
                    self.process_message(msg, send_data_lst)
                    # print('Вызова self.process_message выполнен успешно!')
                except:
                    SERVER_LOGGER.info(f'Связь с клиентом с именем {msg[DESTINATION]} была потеряна')
                    self.clients.remove(self.names[msg[DESTINATION]])
                    del self.names[msg[DESTINATION]]
            self.messages.clear()

    def process_message(self, message, listen_socks):
        """
        Функция обеспечивает адресную отправку сообщения определенному клиенту
        """
        print('сработала ф-ия process_message ')
        if message[DESTINATION] in self.names and self.names[message[DESTINATION]] in listen_socks:
            send_message(self.names[message[DESTINATION]], message)
            SERVER_LOGGER.info(f'Отправлено сообщение пользователю {message[DESTINATION]} '
                               f'от пользователя {message[SENDER]}.')
        elif message[DESTINATION] in self.names and self.names[message[DESTINATION]] not in listen_socks:
            raise ConnectionError
        else:
            SERVER_LOGGER.error(
                f'Пользователь {message[DESTINATION]} не зарегистрирован на сервере, '
                f'отправка сообщения невозможна.')

    def process_client_msg(self, message, client):
        """
        Функция обеспечивает обработку сообщений от клиентов.
        :param message: словарь
        :param client: идентификатор клиента (имя)
        :return:
        """
        SERVER_LOGGER.debug(f'Разбор сообщения от клиента : {message}')
        # Если это сообщение о присутствии, принимаем и отвечаем
        if ACTION in message and message[ACTION] == PRESENCE and TIME in message and USER in message:
            # Если такой пользователь ещё не зарегистрирован, регистрируем,
            # иначе отправляем ответ и завершаем соединение.
            if message[USER][ACCOUNT_NAME] not in self.names.keys():
                self.names[message[USER][ACCOUNT_NAME]] = client
                # Работаем с БД
                client_ip, client_port = client.getpeername()
                self.database.user_login(message[USER][ACCOUNT_NAME], client_ip, client_port)
                # Отправляем сообщение
                send_message(client, RESPONSE_200)
            else:
                response = RESPONSE_400
                response[ERROR] = 'Имя пользователя бьло ранее занято'
                send_message(client, response)
                self.clients.remove(client)
                client.close()
            return
        # Если это сообщение, то добавляем его в очередь сообщений.
        # Ответ не требуется.
        elif ACTION in message and message[ACTION] == MESSAGE and DESTINATION in message and TIME in message \
                and SENDER in message and MESSAGE_TEXT in message:
            self.messages.append(message)
            return
        # Если клиент выходит
        elif ACTION in message and message[ACTION] == EXIT and ACCOUNT_NAME in message:
            # Выполняем метод logout в классе БД
            self.database.user_logout(message[ACCOUNT_NAME])
            # Удялаем клиента
            self.clients.remove(self.names[message[ACCOUNT_NAME]])
            self.names[ACCOUNT_NAME].close()
            del self.names[ACCOUNT_NAME]
            return
        # Иначе отдаём Bad request
        else:
            response = RESPONSE_400
            response[ERROR] = 'Запрос некорректен.'
            send_message(client, response)
            return

def print_help():
    print('Поддерживаемые комманды:')
    print('users - список известных пользователей')
    print('connected - список подключённых пользователей')
    print('loghist - история входов пользователя')
    print('exit - завершение работы сервера.')
    print('help - вывод справки по поддерживаемым командам')


def main():
    """
    Функция получает параметры командной строки, которые были переданы при запуске и
    создает с ними экземпляр класса сервера.
    Далее функция запускает метод main_loop, отвечающий за инициализацию сокета.
    """
    listen_address, listen_port = arg_parser()

    # Инициализируем созданную базу данных
    database = ServerStorage()

    # Запускаем сервер
    server = Server(listen_address, listen_port, database)
    server.daemon = True
    server.start()

    # Основной цикл сервера:
    while True:
        command = input('Введите команду или help: ')
        if command == 'help':
            print_help()
        elif command == 'exit':
            break
        elif command == 'users':
            for user in sorted(database.users_list()):
                print(f'Пользователь {user[0]}, последний вход: {user[1]}')
        elif command == 'connected':
            for user in sorted(database.active_users_list()):
                print(f'Пользователь {user[0]}, подключен: {user[1]}:{user[2]}, время установки соединения: {user[3]}')
        elif command == 'loghist':
            name = input('Введите имя пользователя для просмотра истории. '
                         'Для вывода всей истории, просто нажмите Enter: ')
            for user in sorted(database.login_history(name)):
                print(f'Пользователь: {user[0]} время входа: {user[1]}. Вход с: {user[2]}:{user[3]}')
        else:
            print('Команда не распознана.')


if __name__ == '__main__':
    main()
