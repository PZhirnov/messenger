import inspect
import sys
import logging
import logs.server_log_config
import traceback


def log(func_to_log):
    """ Функция декоратор """
    def log_saver(*args, **kwargs):
        logger_name = 'server' if 'server.py' in sys.argv[0] else 'client'
        LOGGER = logging.getLogger(logger_name)
        rt = func_to_log(*args, *kwargs)

        # к условию по п.1
        LOGGER.debug(f'Была вызвана функция {func_to_log.__name__} с параметрами {args}, {kwargs}')
        # к условию по п.2
        LOGGER.debug(f'Функция {func_to_log.__name__} вызвана '
                     f'из функции {traceback.format_stack()[0].strip().split()[-1]}')

        # LOGGER.debug(f'Была вызвана функция {func_to_log.__name__} с параметрами {args}, {kwargs}'
        #              f'Вызов из модуля {func_to_log.__module__}'
        #              f'Вызов из функции {traceback.format_stack()[0].strip().split()[-1]}')

        return rt
    return log_saver
