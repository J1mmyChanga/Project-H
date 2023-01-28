import os.path
import sys
import traceback
from PyQt5 import QtWidgets
from design import *
from lib import Lib


class Login(QtWidgets.QWidget, LoginWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.register_connections()

    def register_connections(self):
        self.login_pb.clicked.connect(self.check_data)
        self.reg_pb.clicked.connect(self.open_reg)

    def check_data(self):
        num, password = self.number_le.text(), self.password_le.text()
        ###проверка есть ли в бд###

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
        num, password = self.number_reg_le.text(), self.password_reg_le.text()

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
        global nickname
        nicknames = [i[0] for i in self.con.cursor().execute("""SELECT nickname FROM users""").fetchall()]
        emails = [i[0] for i in self.con.cursor().execute("""SELECT email FROM users""").fetchall()]
        name = self.le_name.text()
        nickname = self.le_nickname.text()
        email = self.le_email.text()
        password = self.le_password.text()

        if not (name and nickname and email and password):
            self.raise_exception('Необходимо заполнить все поля!')
            return

        if len(password) < 8 and password:
            self.raise_exception('Пароль должен содержать как минимум 8 символов.')
            return

        if len(list(filter(lambda x: x in "0123456789", password))) < 2 and password:
            self.raise_exception('Пароль должен содержать как минимум 2 цифры.')
            return

        if nickname in nicknames:
            self.raise_exception('Пользователь с таким никнеймом уже существует!')
            return

        if email in emails:
            self.raise_exception('Пользователь с таким адресом электронной почты уже существует!')
            return

        self.con.cursor().execute('''INSERT INTO users(name,nickname,email,password)
                                            VALUES (?,?,?,?)''',
                                  (name, nickname, email, password))
        self.con.cursor().execute(f'''CREATE TABLE {nickname}_clothes (
                                            id      INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                                            clothes INTEGER NOT NULL REFERENCES clothes (clothesid) UNIQUE);''')

        self.con.cursor().execute(f'''CREATE TABLE {nickname}_favourite (
                                            id     INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                                            look   INTEGER REFERENCES looks (looksid) UNIQUE NOT NULL,
                                            output STRING  UNIQUE NOT NULL);''')

        self.con.cursor().execute(f'''CREATE TABLE {nickname}_looks (
                                            id     INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                                            look   INTEGER UNIQUE NOT NULL REFERENCES looks (looksid),
                                            output STRING UNIQUE NOT NULL);''')
        update_session(self.le_nickname.text(), self.le_password.text())
        output_photo = self.convert_to_binary(self.def_picture)
        self.con.cursor().execute('''UPDATE users
                        SET image = ?
                        WHERE nickname = ?''', (output_photo, nickname))
        self.con.commit()

        open_ward()


class YourRecipe(QtWidgets.QWidget, YourRecipeWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.register_connections()

    def register_connections(self):
        self.save_rec_pb.clicked.connect(self.check_data_filled_correctly)

    def check_data_filled_correctly(self):
        global nickname
        nicknames = [i[0] for i in self.con.cursor().execute("""SELECT nickname FROM users""").fetchall()]
        emails = [i[0] for i in self.con.cursor().execute("""SELECT email FROM users""").fetchall()]
        name = self.le_name.text()
        nickname = self.le_nickname.text()
        email = self.le_email.text()
        password = self.le_password.text()

        if not (name and nickname and email and password):
            self.raise_exception('Необходимо заполнить все поля!')
            return

        if len(password) < 8 and password:
            self.raise_exception('Пароль должен содержать как минимум 8 символов.')
            return

        if len(list(filter(lambda x: x in "0123456789", password))) < 2 and password:
            self.raise_exception('Пароль должен содержать как минимум 2 цифры.')
            return

        if nickname in nicknames:
            self.raise_exception('Пользователь с таким никнеймом уже существует!')
            return

        if email in emails:
            self.raise_exception('Пользователь с таким адресом электронной почты уже существует!')
            return

        self.con.cursor().execute('''INSERT INTO users(name,nickname,email,password)
                                            VALUES (?,?,?,?)''',
                                  (name, nickname, email, password))
        self.con.cursor().execute(f'''CREATE TABLE {nickname}_clothes (
                                            id      INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                                            clothes INTEGER NOT NULL REFERENCES clothes (clothesid) UNIQUE);''')

        self.con.cursor().execute(f'''CREATE TABLE {nickname}_favourite (
                                            id     INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                                            look   INTEGER REFERENCES looks (looksid) UNIQUE NOT NULL,
                                            output STRING  UNIQUE NOT NULL);''')

        self.con.cursor().execute(f'''CREATE TABLE {nickname}_looks (
                                            id     INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                                            look   INTEGER UNIQUE NOT NULL REFERENCES looks (looksid),
                                            output STRING UNIQUE NOT NULL);''')
        update_session(self.le_nickname.text(), self.le_password.text())
        output_photo = self.convert_to_binary(self.def_picture)
        self.con.cursor().execute('''UPDATE users
                        SET image = ?
                        WHERE nickname = ?''', (output_photo, nickname))
        self.con.commit()


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
