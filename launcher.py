"""
It is a launcher for starting subprocesses for server_dist and clients of two types: senders and listeners.
for more information:
https://stackoverflow.com/questions/67348716/kill-process-do-not-kill-the-subprocess-and-do-not-close-a-terminal-window
"""

import subprocess


def main():
    """Лаунчер сервера и клиентов для Windows.
    Позволяет пользователю выбрать режим запуска.
    """
    processes = []

    while True:
        action: str = input('Выберите действие: q - выход, '
                            's - запустить сервер и клиенты, k - запустить клиенты, '
                            'x - закрыть все окна: ')

        if action == 'q':
            break

        elif action == 's':
            # Запускаем сервер
            processes.append(subprocess.Popen('python server.py',
                                              creationflags=subprocess.CREATE_NEW_CONSOLE))
        elif action == 'k':
            # Запускаем нужное количество клиентов
            clients_count = int(input('Введите количество тестовых клиентов для запуска: '))
            for i in range(clients_count):
                processes.append(subprocess.Popen(f'python client.py -n test{i + 1} -p 123456',
                                                  creationflags=subprocess.CREATE_NEW_CONSOLE))

        elif action == 'x':
            while processes:
                processes.pop().kill()


if __name__ == '__main__':
    main()
