"""
Пользовательские исключения
"""


class IncorrectDataRecivedError(Exception):
    """
    Некорректные данные получены от сокета
    """
    def __str__(self):
        return 'Принято некорректное сообщение от удаленного компьютера.'


class NonDictInputError(Exception):
    """
    В аргумент функции передан не словарь
    """
    def __str__(self):
        return 'Аргумент функции должен быть словарем.'


class ReqFieldMissingError(Exception):
    """
    Ошибка - отсуствует обязательное поле в принятом словаре
    """
    def __init__(self, missing_field):
        self.missing_field = missing_field

    def __str__(self):
        return f'В принятом словаре отсуствуте обязательное поле {self.missing_field}'


class ServerError(Exception):
    """Исключение - ошибка сервера"""
    def __init__(self, text):
        self.text = text

    def __str__(self):
        return self.text
