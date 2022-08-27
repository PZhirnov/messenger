import socket
import logging
import sys
sys.path.append('../../')

# метод определения модуля, источника запуска.
if sys.argv[0].find('client_dist') == -1:
    #если не клиент то сервер!
    logger = logging.getLogger('server_dist')
else:
    # ну, раз не сервер, то клиент
    logger = logging.getLogger('client_dist')


def log(func_to_log):
    def log_saver(*args , **kwargs):
        logger.debug(f'Была вызвана функция {func_to_log.__name__} c параметрами {args} , {kwargs}. Вызов из модуля {func_to_log.__module__}')
        ret = func_to_log(*args , **kwargs)
        return ret
    return log_saver


def login_required(func):
    """
    Декоратор, проверяющий, что клиент авторизован на сервере.
    Проверяет, что передаваемый объект сокета находится в
    списке авторизованных клиентов.
    За исключением передачи словаря-запроса
    на авторизацию. Если клиент не авторизован,
    генерирует исключение TypeError
    """

    def checker(*args, **kwargs):
        # проверяем, что первый аргумент - экземпляр MessageProcessor
        # Импортить необходимо тут, иначе ошибка рекурсивного импорта.
        # ----------------------------------------------------------------
        # args = (
        #         <MessageProcessor(Thread-5, started daemon 140650633856768)>,
        #         {'action': 'presence',
        #          'time': 1654900198.8001323,
        #           'user': {
        #                    'account_name': 'test1',
        #                    'pubkey': '-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAmKN/CFSxgU8eu0oO0oKw\n29WTZQSfqw/mJgEtr8nLUAOHGcg3kT7epUgPfwbo/V67sJlGhb/UD7dPK81utWRn\nFKhhUGuo+ad/4HnvbSQjIHy2Wbr85T4gJCL1IqTkodAgSOo4Nuv/Qq9r5po0dNIC\nF4YTZrzfCy6V0v349iXM2CXf+/14fHCxsm3OkNCUwHsOW6nzh5fIyAs1UhssJm/Z\nbCNzX5PkRjI7bwBJhoXHNgS1fDyII6vGrQAyAwxU0hKrBAtAzYIon5ZlIYxyF2/5\nKb8IVmLmnrvCpmtjTQ4u80Dp6YuErMCD82GzgUi50UdQoW617AmFxaKpvO7Lu+aA\nfwIDAQAB\n-----END PUBLIC KEY-----'
        #                    }
        #          },
        #          <socket.socket fd=25, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('127.0.0.1', 7777), raddr=('127.0.0.1', 52416)>
        # )
        from server.core import MessageProcessor
        from common.variables import ACTION, PRESENCE
        if isinstance(args[0], MessageProcessor):
            found = False
            for arg in args:
                if isinstance(arg, socket.socket):
                    # Проверяем, что данный сокет есть в списке names класса
                    # MessageProcessor
                    for client in args[0].names:
                        # args[0].names = {'test1': <socket.socket fd=25, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('127.0.0.1', 7777), raddr=('127.0.0.1', 52420)>}
                        if args[0].names[client] == arg:
                            found = True

            # Теперь надо проверить, что передаваемые аргументы не presence
            # сообщение. Если presence, то разрешаем
            for arg in args:
                if isinstance(arg, dict):
                    if ACTION in arg and arg[ACTION] == PRESENCE:
                        found = True
            # Если не не авторизован и не сообщение начала авторизации, то
            # вызываем исключение.
            if not found:
                raise TypeError
        return func(*args, **kwargs)

    return checker
