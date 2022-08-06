"""Лаунчер"""

import subprocess

PROCESSES = []

while True:
    ACTION: str = input('Выберите действие: q - выход, '
                   's - запустить сервер и клиенты, '
                   'x - закрыть все окна: ')

    if ACTION == 'q':
        break
    elif ACTION == 's':
        clients_count = int(input('Введите количество тестовых клиентов для запуска: '))
        PROCESSES.append(subprocess.Popen('python server.py', creationflags=subprocess.CREATE_NEW_CONSOLE))
        for i in range(clients_count):
            PROCESSES.append(subprocess.Popen(f'python client.py -n test{i+1}', creationflags=subprocess.CREATE_NEW_CONSOLE))

    elif ACTION == 'x':
        while PROCESSES:
            PROCESSES.pop().kill()
