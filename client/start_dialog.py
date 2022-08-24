from PyQt5.QtWidgets import QDialog, QPushButton, QLineEdit, QApplication, QLabel, qApp
from PyQt5.QtGui import QFont


class UserNameDialog(QDialog):
    """Класс формы логирования пользователя при входе."""
    def __init__(self):
        super().__init__()

        self.ok_pressed = False

        # Форма
        self.setWindowTitle('Вход в приложение')
        self.setFixedSize(300, 130)

        #  --- Имя пользователя
        self.label = QLabel('Имя пользователя:', self)
        self.label.move(10, 12)
        self.label.setFixedSize(150, 10)
        self.label.setFont(QFont("Arial", 8, QFont.Bold))

        self.client_name = QLineEdit(self)
        self.client_name.move(140, 10)
        self.client_name.setFixedSize(150, 25)

        # --- Пароль
        self.label_passwd = QLabel('Пароль:', self)
        self.label_passwd.move(10, 42)
        self.label_passwd.setFixedSize(150, 20)
        self.label_passwd.setFont(QFont("Arial", 8, QFont.Bold))

        self.client_passwd = QLineEdit(self)
        self.client_passwd.move(140, 48)
        self.client_passwd.setFixedSize(150, 25)
        self.client_passwd.setEchoMode(QLineEdit.Password)

        # кнопки
        self.btn_ok = QPushButton('Начать', self)
        self.btn_ok.move(45, 85)
        self.btn_ok.clicked.connect(self.click)
        self.btn_ok.setFixedSize(100, 30)

        # вторую кнопку делаем по расположению зависимой от первой
        self.btn_cancel = QPushButton('Выход', self)
        self.btn_cancel.move(self.btn_ok.x() + self.btn_ok.width() + 5, self.btn_ok.y())
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
