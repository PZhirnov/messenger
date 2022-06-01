import inspect
import sys
import logging
import traceback

import logs.server_log_config


def log(func_to_log):
    """ Функция декоратор """
    def log_saver(*args, **kwargs):
        logger_name = 'server' if 'server.py' in sys.argv[0] else 'client'
        LOGGER = logging.getLogger(logger_name)
        rt = func_to_log(*args, *kwargs)
        LOGGER.debug(f'Была вызвана функция {func_to_log.__name__} с параметрами {args}, {kwargs}')

        return rt
    return log_saver


print(sys.argv[0])
print(traceback.format_stack())
print(inspect.stack()[0].code_context)