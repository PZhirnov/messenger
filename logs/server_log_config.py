import logging
from logging.handlers import TimedRotatingFileHandler


# Создаем объект-логер с именем 'client'
logger = logging.getLogger('server')

# Создаем объект форматирования:
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s")
# Создаем файловый обработчик логирования
# На стороне сервера реализована ротация лог-файла
fh = TimedRotatingFileHandler('logs/server.log', when='D', interval=1, backupCount=5)

fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
# Добавляем в логгер новый обработчик событий и устанавливаем уровень логирования
logger.addHandler(fh)
logger.setLevel(logging.DEBUG)

if __name__ == '__main__':
    # Создаем потоковый обработчик логирования (по умолчанию sys.stderr):
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    console.setFormatter(formatter)
    logger.addHandler(console)
    logger.info('Тестовый запуск логирования 2')
    logger.critical('test critical')
