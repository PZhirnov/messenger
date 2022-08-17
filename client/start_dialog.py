from PyQt5.QtWidgets import QDialog, QPushButton, QLineEdit, QApplication, QLabel, qApp
from PyQt5.QtCore import QEvent
from PyQt5.QtGui import QFont


# Стартовый диалог с выбором имени пользователя
class UserNameDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.ok_pressed = False

        # Форма
        self.setWindowTitle('Вход в приложение')
        self.setFixedSize(300, 120)

        #  --- Имя пользователя
        self.label = QLabel('Имя пользователя:', self)
        self.label.move(10, 12)
        self.label.setFixedSize(150, 10)
        self.label.setFont(QFont("Arial", 8, QFont.Bold))


        self.client_name = QLineEdit(self)
        self.client_name.move(140, 10)
        self.client_name.setFixedSize(150, 20)

        # --- Пароль
        self.label_pwd = QLabel('Пароль:', self)
        self.label_pwd.move(10, 42)
        self.label_pwd.setFixedSize(150, 20)
        self.label_pwd.setFont(QFont("Arial", 8, QFont.Bold))

        self.client_pwd = QLineEdit(self)
        self.client_pwd.move(140, 48)
        self.client_pwd.setFixedSize(150, 20)
        self.client_pwd.setEchoMode(QLineEdit.Password)


        # кнопки
        self.btn_ok = QPushButton('Начать', self)
        self.btn_ok.move(40, 80)
        self.btn_ok.clicked.connect(self.click)
        self.btn_ok.setFixedSize(100, 30)

        self.btn_cancel = QPushButton('Выход', self)
        self.btn_cancel.move(self.btn_ok.x() + self.btn_ok.width() + 5, 80)
        self.btn_cancel.clicked.connect(qApp.exit)
        self.btn_cancel.setFixedSize(self.btn_ok.width(), self.btn_ok.height())

        self.show()

    # Обработчик кнопки ОК, если поле ввода не пустое, ставим флаг и завершаем приложение.
    def click(self):
        if self.client_name.text():
            self.ok_pressed = True
            qApp.exit()


if __name__ == '__main__':
    app = QApplication([])
    dial = UserNameDialog()
    app.exec_()
