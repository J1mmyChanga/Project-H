import os.path
import sys
import sqlite3
import traceback
from back import BaseWidget
from PyQt5 import QtWidgets
from front.design import *
from back.utils import *

nickname = None


class Login(QtWidgets.QMainWindow, LoginWindow):
    def __init__(self, stacked_widget):
        self.result = None
        super().__init__()
        stacked_widget.addWidget(self)
        self.setupUi(self)

        self.con = sqlite3.connect('db/ETHEREAL_DB.db')

        self.register_connections()

        if os.path.isfile("login.session"):
            username, password = get_session()
            self.le_login.setText(username)
            self.le_password.setText(password)

    def register_connections(self):
        self.pb_login.clicked.connect(self.check_data)
        self.pb_create_account.clicked.connect(self.open_reg)

    def check_data(self):
        global nickname
        self.result = self.con.cursor().execute("""SELECT nickname, password FROM users""").fetchall()
        if (self.le_login.text(), self.le_password.text()) in self.result:
            nickname = self.le_login.text()
            self.le_login.setText('')
            self.le_password.setText('')
            open_ward()
        else:
            self.raise_exception('Неверный логин или пароль: повторите ввод.')
            self.le_login.setText('')
            self.le_password.setText('')

    @staticmethod
    def open_reg():
        registration.le_name.clear()
        registration.le_nickname.clear()
        registration.le_email.clear()
        registration.le_password.clear()
        stak_w.setCurrentWidget(registration)

    @staticmethod
    def raise_exception(text):
        error = QtWidgets.QMessageBox()
        error.setWindowTitle("Ошибка!")
        error.setText(text)
        error.setIcon(QtWidgets.QMessageBox.Warning)
        error.exec()


class Registration(BaseWidget, RegisterWindow):
    def __init__(self, stacked_widget):
        super().__init__(stacked_widget)
        self.setupUi(self)

        self.con = sqlite3.connect('db/ETHEREAL_DB.db')

        self.register_connections()

    def register_connections(self):
        self.pb_to_registrate.clicked.connect(self.check_data_filled_correctly)

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


class Wardrobe(BaseWidget, WardrobeWindow):
    def __init__(self, stacked_widget):
        super().__init__(stacked_widget)
        self.setupUi(self)

        self.con = sqlite3.connect('db/ETHEREAL_DB.db')

        self.register_connections()

    def register_connections(self):
        self.pb_my_profile.clicked.connect(self.open_my_p)
        self.pb_favourite.clicked.connect(open_fav)
        self.pb_styles.clicked.connect(open_st)
        self.pb_add_clothes.clicked.connect(self.open_add_cl)
        self.lw_clothes.itemClicked.connect(self.show_image)

    def open_add_cl(self):
        self.set_data_to_zero()
        stak_w2.show()
        stak_w2.setWindowTitle(adding_clothes.title)
        stak_w2.setCurrentWidget(adding_clothes)

    def open_my_p(self):
        set_data(self)
        stak_w.setWindowTitle(profile.title)
        stak_w.setCurrentWidget(profile)

    @staticmethod
    def set_data_to_zero():
        adding_clothes.cb_chose_clothes.clear()

        adding_clothes.bg_type.setExclusive(False)
        adding_clothes.bg_functionality.setExclusive(False)
        adding_clothes.bg_season.setExclusive(False)

        adding_clothes.rb_upper.setChecked(False)
        adding_clothes.rb_lower.setChecked(False)
        adding_clothes.rb_default.setChecked(False)
        adding_clothes.rb_light.setChecked(False)
        adding_clothes.rb_summer.setChecked(False)
        adding_clothes.rb_winter.setChecked(False)
        adding_clothes.rb_demi.setChecked(False)
        adding_clothes.rb_allseason.setChecked(False)
        adding_clothes.label_set_pic.clear()

        adding_clothes.bg_type.setExclusive(True)
        adding_clothes.bg_functionality.setExclusive(True)
        adding_clothes.bg_season.setExclusive(True)

        adding_clothes.clothes_type = ''
        adding_clothes.clothes_functionality = ''
        adding_clothes.clothes_season = ''

    def show_image(self):
        pic_name = self.con.cursor().execute('''SELECT clothesid FROM clothes
                                                WHERE name = ?''', (self.lw_clothes.currentItem().text(),)).fetchone()
        try:
            pixmap = QPixmap(f'front/clothes_def/{pic_name[0]}.png')
            self.label_set_pic.setScaledContents(True)
            self.label_set_pic.setPixmap(pixmap)
        except TypeError:
            pass


class Profile(BaseWidget, ProfileWindow):
    def __init__(self, stacked_widget):
        super().__init__(stacked_widget)
        self.check_is_changed_file = False
        self.setupUi(self)

        self.non_def_picture = None
        self.pixmap = None

        self.con = sqlite3.connect('db/ETHEREAL_DB.db')

        self.register_connections()

    def register_connections(self):
        self.pb_wardrobe.clicked.connect(open_ward)
        self.pb_favourite.clicked.connect(open_fav)
        self.pb_styles.clicked.connect(open_st)
        self.pb_logout.clicked.connect(open_log)
        self.pb_save_data.clicked.connect(self.save_data)
        self.pb_chose_file.clicked.connect(self.file_selection)

    def file_selection(self):
        self.non_def_picture = QtWidgets.QFileDialog.getOpenFileName(
            self, 'Выбрать картинку', '',
            'Картинка (*.jpg);;Картинка (*.png);;Все файлы (*)')[0]
        self.pixmap = QPixmap(self.non_def_picture)
        self.check_is_changed_file = True
        self.label_picture.setScaledContents(True)
        self.label_picture.setPixmap(self.pixmap)

    def save_data(self):
        if self.check_is_changed_file:
            self.def_picture = self.non_def_picture
            self.check_is_changed_file = False
        if self.le_name_edit.text() != '':
            self.con.cursor().execute('''UPDATE users
                            SET name = ?
                            WHERE nickname = ?''', (self.le_name_edit.text(), nickname))
        if self.le_email_edit.text() != '':
            emails = [i[0] for i in self.con.cursor().execute("""SELECT email FROM users""").fetchall()]
            if self.le_email_edit.text() in emails:
                self.raise_exception('Пользователь с таким адресом электронной почты уже существует!')
                self.le_email_edit.setText('')
            else:
                self.con.cursor().execute('''UPDATE users
                                SET email = ?
                                WHERE nickname = ?''', (self.le_email_edit.text(), nickname))
        output_photo = self.convert_to_binary(self.def_picture)
        self.con.cursor().execute('''UPDATE users
                        SET image = ?
                        WHERE nickname = ?''', (output_photo, nickname))
        n_e = users_data(self)
        self.le_name_edit.setPlaceholderText(n_e[0][0])
        self.le_email_edit.setPlaceholderText(n_e[0][1])
        self.le_name_edit.setText('')
        self.le_email_edit.setText('')
        self.con.commit()


class Favourite(BaseWidget, FavouriteWindow):
    def __init__(self, stacked_widget):
        super().__init__(stacked_widget)

        self.setupUi(self)

        self.con = sqlite3.connect('db/ETHEREAL_DB.db')

        self.pb_wardrobe.clicked.connect(open_ward)
        self.pb_styles.clicked.connect(open_st)
        self.pb_my_profile.clicked.connect(self.open_my_p)
        self.pb_del.clicked.connect(self.delete_look)
        self.lw_clothes.itemClicked.connect(self.to_show_image)

        self.register_connections()

    def open_my_p(self):
        set_data(self)
        stak_w.setWindowTitle(profile.title)
        stak_w.setCurrentWidget(profile)

    def delete_look(self):
        favourite.label_set_pic1.clear()
        favourite.label_set_pic2.clear()
        favourite.label_set_pic3.clear()
        look = self.lw_clothes.currentItem()
        if look is None:
            self.raise_exception('Выберите образ, который хотите удалить из избранного!')
        else:
            self.con.cursor().execute(f'''DELETE FROM {nickname}_favourite
                                            WHERE output = ?''', (look.text(),))
            self.lw_clothes.clear()
            self.lw_clothes.addItems(
                [i[0] for i in self.con.cursor().execute(f'''SELECT output FROM {nickname}_favourite''').fetchall()])
            self.con.commit()

    def to_show_image(self):
        show_image(self)


class Styles(BaseWidget, StylesWindow):
    def __init__(self, stacked_widget):
        super().__init__(stacked_widget)

        self.setupUi(self)

        self.con = sqlite3.connect('db/ETHEREAL_DB.db')

        self.register_connections()

    def register_connections(self):
        self.pb_wardrobe.clicked.connect(open_ward)
        self.pb_favourite.clicked.connect(open_fav)
        self.pb_my_profile.clicked.connect(self.open_my_p)
        self.pb_settings.clicked.connect(self.open_looks_settings)
        self.pb_dob.clicked.connect(self.add_to_favourite)
        self.lw_clothes.itemClicked.connect(self.to_show_image)

    @staticmethod
    def open_looks_settings():
        settings.bg_style.setExclusive(False)
        settings.bg_season.setExclusive(False)

        settings.rb_sport.setChecked(False)
        settings.rb_business.setChecked(False)
        settings.rb_casual.setChecked(False)
        settings.rb_summer.setChecked(False)
        settings.rb_winter.setChecked(False)
        settings.rb_demi.setChecked(False)

        settings.bg_style.setExclusive(True)
        settings.bg_season.setExclusive(True)

        stak_w2.show()
        stak_w2.setWindowTitle(settings.title)
        stak_w2.setCurrentWidget(settings)

    def open_my_p(self):
        set_data(self)
        stak_w.setWindowTitle(profile.title)
        stak_w.setCurrentWidget(profile)

    def add_to_favourite(self):
        if self.lw_clothes.currentItem() is None:
            self.raise_exception('Выберите образ, который хотите добавить в избранное!')
        else:
            look = self.lw_clothes.currentItem().text()
            look_id = self.con.cursor().execute(f'''SELECT look FROM {nickname}_looks
                                                    WHERE output = ?''', (look,)).fetchone()[0]
            if look_id not in [j[0] for j in
                               self.con.cursor().execute(f'''SELECT look from {nickname}_favourite''').fetchall()]:
                self.con.cursor().execute(f'''INSERT INTO {nickname}_favourite(look, output) VALUES(?,?)''',
                                          (look_id, look))
                self.con.commit()
            else:
                self.raise_exception('Этот образ уже есть в избранном!')

    def to_show_image(self):
        show_image(self)


class AddingClothes(BaseWidget, AddingClothesWindow):
    def __init__(self):
        super().__init__()

        self.setupUi(self)

        self.con = sqlite3.connect('db/ETHEREAL_DB.db')

        self.clothes_functionality = None
        self.clothes_season = None
        self.clothes_type = None

        self.register_connections()

    def register_connections(self):
        self.pb_search_for_clothes.clicked.connect(self.find_clothes)
        self.pb_add_clothes.clicked.connect(self.clothes_selection)
        self.cb_chose_clothes.currentTextChanged.connect(self.show_image)

    def find_clothes(self):
        all_radio_buttons_checked = True

        if self.bg_type.checkedButton() is None:
            all_radio_buttons_checked = False
        else:
            self.clothes_type = self.bg_type.checkedButton().text()

        if self.bg_functionality.checkedButton() is None:
            all_radio_buttons_checked = False
        else:
            self.clothes_functionality = self.bg_functionality.checkedButton().text()

        if self.bg_season.checkedButton() is None:
            all_radio_buttons_checked = False
        else:
            self.clothes_season = self.bg_season.checkedButton().text()

        if self.clothes_type == 'Поясная' and self.clothes_functionality == 'Верхняя лёгкая':
            self.raise_exception('Для добавления поясной одежды, параметр функциональность должен быть "Верхняя"')

        matching_clothes = [i[0] for i in self.con.cursor().execute(
            '''SELECT name from clothes
                WHERE typeid IN (
                SELECT typeid from type
                WHERE name=?)
                and funcid IN (
                SELECT funcid from func
                WHERE name=?)
                and seasonid IN (
                SELECT seasonid from season
                WHERE name=?)''',
            (self.clothes_type, self.clothes_functionality, self.clothes_season)).fetchall()]

        if all_radio_buttons_checked:
            self.cb_chose_clothes.clear()
            self.cb_chose_clothes.addItems(matching_clothes)
        else:
            self.raise_exception('Необходимо указать все параметры!')

    def clothes_selection(self):
        cb_clothes = self.cb_chose_clothes.currentText()
        if cb_clothes not in get_clothes():
            if cb_clothes:
                clothes_id = self.con.cursor().execute('''SELECT clothesid from clothes
                                                            WHERE name=?''',
                                                       (cb_clothes,)).fetchall()[0][0]
                self.con.cursor().execute(f'''INSERT INTO {nickname}_clothes(clothes)
                                                VALUES(?)''', (clothes_id,))
                wardrobe.lw_clothes.addItem(cb_clothes)
                wardrobe.lw_clothes.sortItems()
                self.con.commit()
                stak_w2.close()
            else:
                self.raise_exception('Необходимо указать все параметры и цвет!')
        else:
            self.raise_exception('Этот предмет уже есть в вашем гардеробе!')

    def show_image(self):
        pic_name = self.con.cursor().execute('''SELECT clothesid FROM clothes
                                                WHERE name = ?''', (self.cb_chose_clothes.currentText(),)).fetchone()
        try:
            pixmap = QPixmap(f'front/clothes_def/{pic_name[0]}.png')
            self.label_set_pic.setScaledContents(True)
            self.label_set_pic.setPixmap(pixmap)
        except TypeError:
            pass

    def raise_exception(self, text):
        error = QtWidgets.QMessageBox()
        error.setWindowTitle("Ошибка!")
        error.setText(text)
        error.setIcon(QtWidgets.QMessageBox.Warning)
        error.exec()


class Settings(BaseWidget, StylesSettingsWindow):
    def __init__(self):
        super().__init__()

        self.setupUi(self)

        self.con = sqlite3.connect('db/ETHEREAL_DB.db')

        self.register_connections()

    def register_connections(self):
        self.pb_chose_style.clicked.connect(self.looks_selection)

    def looks_selection(self):
        styles.label_set_pic1.clear()
        styles.label_set_pic2.clear()
        styles.label_set_pic3.clear()

        if self.bg_style.checkedButton() is None:
            style = '%'
        else:
            style = str(self.con.cursor().execute('''SELECT styleid from style 
                                                WHERE name = ?''', (self.bg_style.checkedButton().text(),)).fetchone()[
                            0])
        if self.bg_season.checkedButton() is None:
            season = '%'
        else:
            season = str(self.con.cursor().execute('''SELECT seasonid from season 
                                                WHERE name_looks = ?''',
                                                   (self.bg_season.checkedButton().text(),)).fetchone()[0])
        proper_looks = [i[0] for i in self.con.cursor().execute(f'''SELECT output from {nickname}_looks 
                                                WHERE look IN (
                                                SELECT looksid FROM looks
                                                WHERE styleid LIKE ?
                                                AND seasonid LIKE ?)''', (style, season)).fetchall()]
        styles.lw_clothes.clear()
        styles.lw_clothes.addItems(proper_looks)
        stak_w2.hide()


def excepthook(exc_type, exc_value, exc_tb):
    tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
    print("Detected an error !: " + tb)


def open_ward():
    wardrobe.label_set_pic.clear()
    wardrobe.lw_clothes.clear()
    wardrobe.lw_clothes.addItems(get_clothes())
    stak_w.setWindowTitle(wardrobe.title)
    stak_w.setCurrentWidget(wardrobe)


def open_fav():
    favourite.label_set_pic1.clear()
    favourite.label_set_pic2.clear()
    favourite.label_set_pic3.clear()
    con = sqlite3.connect('db/ETHEREAL_DB.db')
    favourite.lw_clothes.clear()
    favourite.lw_clothes.addItems(
        [i[0] for i in con.cursor().execute(f'''SELECT output FROM {nickname}_favourite''').fetchall()])
    stak_w.setWindowTitle(favourite.title)
    stak_w.setCurrentWidget(favourite)


def open_st():
    styles.label_set_pic1.clear()
    styles.label_set_pic2.clear()
    styles.label_set_pic3.clear()
    styles.lw_clothes.clear()
    styles.lw_clothes.addItems(complete_looks())
    stak_w.setWindowTitle(styles.title)
    stak_w.setCurrentWidget(styles)


def open_log():
    stak_w.setWindowTitle(login.title.text())
    stak_w.setCurrentWidget(login)


def set_data(object_):
    profile.check_is_changed_file = False
    n_e = users_data(object_)
    profile.le_name_edit.setText('')
    profile.le_email_edit.setText('')
    profile.le_name_edit.setPlaceholderText(n_e[0][0])
    profile.le_email_edit.setPlaceholderText(n_e[0][1])
    profile.label_nickname.setText(nickname)
    bytes_array = object_.con.cursor().execute('''SELECT image from users WHERE nickname = ?''',
                                               (nickname,)).fetchone()[0]
    profile.pixmap = QPixmap(profile.convert_to_image(bytes_array, 'img.png'))
    profile.label_picture.setScaledContents(True)
    profile.label_picture.setPixmap(profile.pixmap)


def users_data(object_):
    name_email = object_.con.cursor().execute('''SELECT name, email from users
                                         WHERE nickname = ?''', (nickname,)).fetchall()
    return name_email


def get_clothes():
    con = sqlite3.connect('db/ETHEREAL_DB.db')
    cur = con.cursor()
    clothes = cur.execute(f'''SELECT name FROM clothes
                                INNER JOIN {nickname}_clothes
                                ON {nickname}_clothes.clothes = clothes.clothesid''').fetchall()
    clothes = [i[0] for i in clothes]
    return sorted(clothes)


def complete_looks():
    con = sqlite3.connect('db/ETHEREAL_DB.db')
    cur = con.cursor()
    looks = cur.execute(f'''SELECT first, second, lower, styleid, looksid
                            FROM looks
                            WHERE (first IN (SELECT clothes FROM {nickname}_clothes)
                            AND second IN (SELECT clothes FROM {nickname}_clothes)
                            AND lower IN (SELECT clothes FROM {nickname}_clothes))
                            OR (first IS NULL
                            AND second IN (SELECT clothes FROM {nickname}_clothes)
                            AND lower IN (SELECT clothes FROM {nickname}_clothes))''').fetchall()
    return convert_to_lw_items(looks)


def convert_to_lw_items(looks):
    sp = []
    con = sqlite3.connect('db/ETHEREAL_DB.db')
    cur = con.cursor()
    for i in looks:
        a = []
        for j in range(5):
            if j < 3:
                item = cur.execute(f'''SELECT name FROM clothes
                                    WHERE clothesid = ?''', (i[j],)).fetchone()
                if item is not None:
                    a.append(item[0])
            elif j == 3:
                a.insert(0, cur.execute(f'''SELECT name FROM style
                                    WHERE styleid = ?''', (i[j],)).fetchone()[0])
            elif j == 4:
                a.insert(0, i[j])
        sp.append(a)
    sp = sorted(sp, key=lambda x: x[1])
    for i in range(len(sp)):
        look_id = sp[i][0]
        look = ', '.join(sp[i][2:])
        sp[i] = f'{sp[i][1]}: {look.lower()}'
        if look_id not in [j[0] for j in cur.execute(f'''SELECT look from {nickname}_looks''').fetchall()]:
            cur.execute(f'''INSERT INTO {nickname}_looks(look, output) VALUES(?,?)''', (look_id, sp[i]))
            con.commit()
    return sp


def show_image(object_):
    object_.label_set_pic1.clear()
    object_.label_set_pic2.clear()
    object_.label_set_pic3.clear()
    look = object_.lw_clothes.currentItem().text()
    clothes = [i.strip() for i in look[look.index(':') + 1:].split(',')]

    if len(clothes) > 2:
        pic_name = object_.con.cursor().execute('''SELECT clothesid FROM clothes
                                                WHERE name = ?''',
                                                (clothes[0].capitalize(),)).fetchone()
        pixmap = QPixmap(f'front/clothes_def/{pic_name[0]}.png')
        object_.label_set_pic1.setScaledContents(True)
        object_.label_set_pic1.setPixmap(pixmap)

    pic_name = object_.con.cursor().execute('''SELECT clothesid FROM clothes
                                            WHERE name = ?''', (clothes[-2].capitalize(),)).fetchone()
    pixmap = QPixmap(f'front/clothes_def/{pic_name[0]}.png')
    object_.label_set_pic2.setScaledContents(True)
    object_.label_set_pic2.setPixmap(pixmap)

    pic_name = object_.con.cursor().execute('''SELECT clothesid FROM clothes
                                            WHERE name = ?''', (clothes[-1].capitalize(),)).fetchone()
    pixmap = QPixmap(f'front/clothes_def/{pic_name[0]}.png')
    object_.label_set_pic3.setScaledContents(True)
    object_.label_set_pic3.setPixmap(pixmap)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    stak_w2 = QtWidgets.QStackedWidget()
    adding_clothes = AddingClothes()
    settings = Settings()
    stak_w2.addWidget(adding_clothes)
    stak_w2.addWidget(settings)
    stak_w2.setFixedSize(750, 1024)
    stak_w2.move(585, 0)
    stak_w2.setStyleSheet("QWidget{background:#57AD8E}")

    stak_w = QtWidgets.QStackedWidget()
    login = Login(stak_w)
    registration = Registration(stak_w)
    wardrobe = Wardrobe(stak_w)
    profile = Profile(stak_w)
    favourite = Favourite(stak_w)
    styles = Styles(stak_w)

    stak_w.setCurrentIndex(0)
    stak_w.setWindowTitle('ETHEREAL')
    stak_w.show()
    stak_w.setFixedSize(1440, 1024)
    stak_w.move(240, 0)
    stak_w.setStyleSheet("QWidget{background:#57AD8E}")

    sys.excepthook = excepthook
    sys.exit(app.exec_())