import os.path
import requests
import sys
import traceback
from PyQt5 import QtWidgets
from design import *
from lib import Lib

number = ""


class Login(QtWidgets.QWidget, LoginWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.register_connections()

    def register_connections(self):
        self.login_pb.clicked.connect(self.check_data)
        self.reg_pb.clicked.connect(self.open_reg)

    def check_data(self):
        global number
        num, password = self.number_le.text(), self.password_le.text()
        number = num
        if Lib.check_password(num, password):
            open_settings()
        else:
            raise_exception("Некорректные данные")
            self.number_le.setText('')
            self.password_le.setText('')

    @staticmethod
    def open_reg():
        registration.number_reg_le.clear()
        registration.password_reg_le.clear()
        stak.setCurrentWidget(registration)


class Registration(QtWidgets.QWidget, RegisterWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.register_connections()

    def register_connections(self):
        self.create_acc_pb.clicked.connect(self.check_data_filled_correctly)

    def check_data_filled_correctly(self):
        global number
        num, password = self.number_reg_le.text(), self.password_reg_le.text()
        number = num
        if len(num) != 12 or not num.startswith('+79'):
            raise_exception('Некорректно введён номер телефона')
            self.number_reg_le.setText('')
            self.password_reg_le.setText('')
        elif len(password) < 6:
            raise_exception('Слишком короткий пароль')
        else:
            Lib.register(num, password)
            open_settings()


class Settings(QtWidgets.QWidget, SettingsWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.register_connections()

    def register_connections(self):
        self.find_rec_pb.clicked.connect(self.check_data_filled_correctly)

    def check_data_filled_correctly(self):
        global per
        all_bg_checked = True
        d = {
            'Кино': 1,
            'Вечеринка': 2,
            'Просто хочу поесть': 3,
            'Просто и со вкусом': 4,
            'Что-то посложнее': 5,
            'Мясо': 6,
            'Рыба': 7,
            'Салат': 8,
            'Паста': 9,
            'Десерт': 10,
            'Не надо мыть посуду': 11,
            'Закуска': 12
        }

        if self.plans_bg.checkedButton() is None:
            all_bg_checked = False
        else:
            self.plans = d[self.plans_bg.checkedButton().text()]

        if self.dif_level_bg.checkedButton() is None:
            all_bg_checked = False
        else:
            self.dif_level = d[self.dif_level_bg.checkedButton().text()]

        if self.preferences_bg.checkedButton() is None:
            all_bg_checked = False
        else:
            self.preferences = d[self.preferences_bg.checkedButton().text()]

        # work with db

        if all_bg_checked:
            a = Lib.get_recipe(self.plans, self.dif_level, self.preferences)
            per = a
            your_recipe.rec_plain_edit.setPlainText(per["name"])
            self.open_recipe()
        else:
            self.raise_exception('Необходимо указать все параметры!')

    def open_recipe(self):
        stak.setCurrentWidget(your_recipe)


class YourRecipe(QtWidgets.QWidget, YourRecipeWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.register_connections()

    def register_connections(self):
        self.save_rec_pb.clicked.connect(self.check_data_filled_correctly)

    def check_data_filled_correctly(self):
        user_id = Lib.get_user_by_phone(number)
        Lib.set_last_recipe_request(user_id, per)


def excepthook(exc_type, exc_value, exc_tb):
    tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
    print("Detected an error !: " + tb)


def raise_exception(text):
    error = QtWidgets.QMessageBox()
    error.setWindowTitle("Ошибка!")
    error.setText(text)
    error.setIcon(QtWidgets.QMessageBox.Warning)
    error.exec()


def open_settings():
    stak.setCurrentWidget(settings)


per = {'id': 0, 'name': '0'}
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    stak = QtWidgets.QStackedWidget()
    stak.setFixedSize(820, 1024)
    stak.move(585, 0)
    stak.setStyleSheet("QWidget{background:#C3A995}")

    login = Login()
    stak.addWidget(login)
    registration = Registration()
    stak.addWidget(registration)
    settings = Settings()
    stak.addWidget(settings)
    your_recipe = YourRecipe()
    stak.addWidget(your_recipe)

    stak.setCurrentIndex(0)
    stak.setWindowTitle('JustEatIt')
    stak.show()

    sys.excepthook = excepthook
    sys.exit(app.exec_())
