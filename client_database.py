from sqlalchemy import create_engine, Table, Column, Integer, String, Text, MetaData, DateTime
from sqlalchemy.orm import mapper, sessionmaker
from common.variables import *
from datetime import datetime


# Класс базы данных клиента
class ClientDatabase:

    # Класс - отображение таблицы известных пользователей
    class KnownUsers:
        def __init__(self, user):
            self.id = None
            self.username = user

    # Класс - отображение таблицы истории сообщений
    class MessageHistory:
        def __init__(self, from_user, to_user, message):
            self.id = None
            self.from_user = from_user
            self.to_user = to_user
            self.message = message
            self.date = datetime.now()

    # Класс - отображение списка контактов
    class Contacts:
        def __init__(self, contact):
            self.id = None
            self.name = contact

    # ------------- Работа с методами класса ClientDatabase ------
    def __init__(self, name):
        # Создаем движок БД. Каждый клиент имеет свою БД, т.к. разрешено несколько клиентов.
        # echo передаем False, учитывая мультипоточность клиента
        self.database_engine = create_engine(f'sqlite:///client_{name}.db3',
                                             echo=False,
                                             pool_recycle = 7200,
                                             connect_args={'check_same_thread': False})
        # Создаем Metadata()
        self.metadata = MetaData()

        # Создаем таблицу известных пользователей
        users = Table('known_users', self.metadata,
                      Column('id', Integer, primary_key=True),
                      Column('username', String)
                      )

        # Создаем таблицу истории сообщений
        history = Table('message_history', self.metadata,
                        Column('id', Integer, primary_key=True),
                        Column('from_user', String),
                        Column('to_user', String),
                        Column('message', Text),
                        Column('date', DateTime)
                        )

        # Создаем таблицу контактов
        contacts = Table('contacts', self.metadata,
                         Column('id', Integer, primary_key=True),
                         Column('name', String, unique=True)
                         )

        # Создаем таблицы
        self.metadata.create_all(self.database_engine)

        # Создаем отображения
        mapper(self.KnownUsers, users)
        mapper(self.MessageHistory, history)
        mapper(self.Contacts, contacts)

        # Создаем сессию
        Session = sessionmaker(bind=self.database_engine)
        self.session = Session()

        # Очищаем таблицу контактов
        self.session.query(self.Contacts).delete()
        self.session.commit()

    # Функция для добавления контактов
    def add_contact(self, contact):
        if not self.session.query(self.Contacts).filter_by(name=contact).count():
            contact_row = self.Contacts(contact)
            self.session.add(contact_row)
            self.session.commit()

    # Функция удаления контакта
    def del_contact(self, contact):
        self.session.query(self.Contacts).filter_by(name=contact).delete()
        self.session.commit()

    # Добавление известных пользователей. Пользователия получаются с сервера
    def add_users(self, users_list):
        self.session.query(self.KnownUsers).delete()
        for user in users_list:
            user_row = self.KnownUsers(user)
            self.session.add(user_row)
        self.session.commit()

    # Функция сохраняет сообщения
    def save_message(self, from_user, to_user, message):
        message_row = self.MessageHistory(from_user, to_user, message)
        self.session.add(message_row)
        self.session.commit()




