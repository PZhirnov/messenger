
"""Лаунчер"""

import subprocess

PROCESSES = []

while True:
    ACTION: str = input('Выберите действие: q - выход, '
                   's - запустить сервер и клиенты, k - запустить клиенты, '
                   'x - закрыть все окна: ')

    if ACTION == 'q':
        break

    elif ACTION == 's':
        # Запускаем сервер
        PROCESSES.append(subprocess.Popen('python server.py',
                                          creationflags=subprocess.CREATE_NEW_CONSOLE))
    elif ACTION == 'k':
        # Запускаем нужное количество клиентов
        clients_count = int(input('Введите количество тестовых клиентов для запуска: '))
        for i in range(clients_count):
            PROCESSES.append(subprocess.Popen(f'python client.py -n test{i+1}',
                                              creationflags=subprocess.CREATE_NEW_CONSOLE))

    elif ACTION == 'x':
        while PROCESSES:
            PROCESSES.pop().kill()
