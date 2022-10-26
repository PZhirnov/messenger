Серверный модуль
================

Серверная часть приложения для обмена сообщениями.
Обеспечивает подключение и обмен сообщениями между клиентами.
Позволяет администратору управлять пользователями.

Поддерживает аргументы командной строки:

``python server.py {имя сервера} {порт} -n или --name {имя пользователя} -p или -password {пароль}``

1. -a - адрес сервера сообщений (127.0.0.1 по умолчанию).
2. -p - порт для подключения клиентов (7777 по умолчанию)
3. --no_gui - использовать в случае, если не требуется отобразить интерфейс сервера.

Все опции командной строки являются необязательными.

Примеры использования:

* ``python server.py``

*Запуск приложения с параметрами по умолчанию.*

* ``python ыукмук.py -p ip_address -p port``

*Запуск приложения с указанием адреса и порта.*

Вид главного окна:

.. image:: /_static/server_main_window.png


* ``python client.py -p ip_address -p port --no_gui``
*Запуск сервера без интерфейса*

main_window.py
~~~~~~~~~~~~~~

.. autoclass:: server.main_window.MainWindow
	:members:


add_user.py
~~~~~~~~~~~

.. autoclass:: server.add_user.RegisterUser
	:members:

Вид окна регистрации:

.. image:: /_static/server_add_user.png


remove_user.py
~~~~~~~~~~~~~~

.. autoclass:: server.remove_user.DelUserDialog
	:members:

Вид окна удаления пользователя:

.. image:: /_static/server_delete_user.png


stat_window.py
~~~~~~~~~~~~~~

.. autoclass:: server.stat_window.StatWindow
	:members:

database.py
~~~~~~~~~~~~~~

.. autoclass:: server.database.ServerStorage
	:members:

