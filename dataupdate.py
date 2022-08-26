import requests
import sqlite3 as sq


import keyboards

modern_authors = tuple()
classic_authors = tuple()
stack_size = {}


def data_upd():
    """
    При старте программы или запуске из режима админа обновляет базу данных
    """
    database_upd = open('data.db', 'wb')
    upd = requests.get('https://drive.google.com/uc?export=download&id=1EIU2yTyCKs9S2xNRoXCqDr2foEVskICE')
    database_upd.write(upd.content)
    database_upd.close()
    authors_upd()
    keyboards.keyboards_create()
    stack_size_upd()


def authors_upd():
    """
    Эта функция запускается при старте приложения, либо из режима админа, берет из актуальной БД список авторов
    и из него формирует пользовательские клавиатуры современных и классических художников
    """
    global modern_authors
    global classic_authors
    with sq.connect('data.db') as con:
        cur = con.cursor()
        cur.execute("SELECT author FROM authors WHERE style == 'modern' GROUP BY author")
        modern_authors = cur.fetchall()
        modern_authors = [x[0] for x in modern_authors]  # Переводим кортежи из списка в строки, база возвращает кортеж
        keyboards.keyboard_create(modern_authors, classic=False)
    with sq.connect('data.db') as con:
        cur = con.cursor()
        cur.execute("SELECT author FROM authors WHERE style == 'classic' GROUP BY author")
        classic_authors = cur.fetchall()
        classic_authors = [x[0] for x in classic_authors]
        keyboards.keyboard_create(classic_authors, classic=True)


def stack_size_upd():
    """
    Данная функция вычисляет минимальный размер стека в котором хранятся изображения отправленные пользователю,
    нужно для того чтобы присылаемые ботом картины не повторялись насколько это возможно долго
    """
    with sq.connect('data.db') as con:
        cur = con.cursor()
        cur.execute("SELECT count(author) FROM pic GROUP BY author ORDER BY count(author) LIMIT 1 ")
        stack_min = cur.fetchall()
        stack_size['min'] = stack_min[0][0] - 1
