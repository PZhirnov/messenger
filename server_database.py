from datetime import datetime
from common.variables import *
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, DateTime, ForeignKey
from sqlalchemy.orm import mapper, sessionmaker



# Класс серверной базы данных
class ServerStorage:
    # --- Классы отображения таблиц с данными ---
    # Пользователи
    class AllUsers:
        def __init__(self, username):
            self.id = None
            self.name = username
            self.last_login = datetime.now()

    # Активные пользователи
    class ActiveUsers:
        def __init__(self, user_id, ip_address, port, login_time):
            self.id = None
            self.user = user_id
            self.ip_address = ip_address
            self.port = port
            self.login_time = login_time

    # История входов
    class LoginHistory:
        def __init__(self, name, date, ip, port):
            self.id = None
            self.name = name
            self.date_time = date
            self.ip = ip
            self.port = port

    # --- Работа с БД ---

    def __init__(self):
        # -- Создаём движок базы данных
        self.database_engine = create_engine(SERVER_DATABASE, echo=False, pool_recycle=7200)
        self.metadata = MetaData()

        # -- Описываем структуру таблиц БД
        user_table = Table('Users', self.metadata,
                           Column('id', Integer, primary_key=True),
                           Column('name', String, unique=True),
                           Column('last_login', DateTime),
                           )
        active_users_table = Table('Active_users', self.metadata,
                                   Column('id', Integer, primary_key=True),
                                   Column('user', ForeignKey('Users.id'), unique=True),
                                   Column('ip_address', String),
                                   Column('port', Integer),
                                   Column('login_time', DateTime),
                                   )
        user_login_history = Table('Login_history', self.metadata,
                                   Column('id', Integer, primary_key=True),
                                   Column('name', ForeignKey('Users.id')),
                                   Column('date_time', DateTime),
                                   Column('ip', String),
                                   Column('port', String),
                                   )
        # -- Создаем таблицы
        self.metadata.create_all(self.database_engine)

        # -- Создаем отображения и связываем классы в ORM с таблицами
        mapper(self.AllUsers, user_table)
        mapper(self.ActiveUsers, active_users_table)
        mapper(self.LoginHistory, user_login_history)

        # -- Создаем сессию
        Session = sessionmaker(bind=self.database_engine)
        self.session = Session()

        # перед началом работы очищаем таблицу с активными пользователями
        self.session.query(self.ActiveUsers).delete()
        self.session.commit()

    # Функция, обрабатывающая вход пользователя
    def user_login(self, username, ip_address, port):
        """
        Функция проверяет наличие пользователя в БД и фиксируется факт входа
        """
        print(username, ip_address, port)

        # -- Проверим наличие пользователя в БД и если нет, то создадим
        users_in_bd = self.session.query(self.AllUsers).filter_by(name=username)
        # TODO корретность условия при проверке
        if users_in_bd.count():
            user = users_in_bd.first()
            user.last_login = datetime.now()
        else:
            user = self.AllUsers(username)
            self.session.add(user)
            self.session.commit()  # сохранить, чтобы потом получать id

        # -- Добавляем запись в таблицу активных пользователей
        new_active_user = self.ActiveUsers(user.id, ip_address, port, datetime.now())
        self.session.add(new_active_user)

        # -- Добавляем запись в историю логирования
        history = self.LoginHistory(user.id, datetime.now(), ip_address, port)
        self.session.add(history)

        # -- Сохраняем все изменения
        self.session.commit()

    def user_logout(self, username):
        """
        Функция, фиксирующая отключение пользователя от сервера
        """
        # Получаем пользователя из таблицы пользователей
        user = self.session.query(self.AllUsers). filter_by(name=username).first()
        # Удаляем пользователя из таблицы активных пользователей
        self.session.query(self.ActiveUsers).filter_by(user=user.id).delete()
        # Сохраняем изменения
        self.session.commit()


    def users_list(self):
        """
        Функция возвращает список известных пользователей со временем последнего входа
        """
        query = self.session.query(
            self.AllUsers.name,
            self.AllUsers.last_login
        )
        return query.all()

    def active_users_list(self):
        """
        Функция возвращает список активных пользователей
        """
        # Делаем JOIN запрос к связанным таблицам - ALLUsers и ActiveUsers
        query = self.session.query(
            self.AllUsers.name,
            self.ActiveUsers.ip_address,
            self.ActiveUsers.port,
            self.ActiveUsers.login_time
        ).join(self.AllUsers)
        return query.all()

    def login_history(self, username=None):
        """
        Получим историю входа по пользователю / всем пользвателям
        """
        query = self.session.query(self.AllUsers.name,
                                   self.LoginHistory.date_time,
                                   self.LoginHistory.ip,
                                   self.LoginHistory.port
                                   ).join(self.AllUsers)
        if username:
            query = query.filter(self.AllUsers.name == username)
        return query.all()


# Отладка
if __name__ == '__main__':
    # инициализируем класс БД
    test_db = ServerStorage()
    # подключаем клиентов
    test_db.user_login('client_1', '192.168.1.4', 8080)
    test_db.user_login('client_2', '192.168.1.5', 7777)
    # покажем активных пользователей
    print(' ---- test_db.active_users_list() ----')
    print(test_db.active_users_list())

    # Выполняем "отключение" пользователя
    test_db.user_logout('client_1')
    # И выводим список активных пользователей
    print(' ---- test_db.active_users_list() after logout client_1 ----')
    print(test_db.active_users_list())

    # Запрашиваем историю входов по пользователю
    print(' ---- test_db.login_history(client_1) ----')
    print(test_db.login_history('client_1'))

    # и выводим список известных пользователей
    print(' ---- test_db.users_list() ----')
    print(test_db.users_list())
