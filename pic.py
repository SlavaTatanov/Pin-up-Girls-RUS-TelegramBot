import sqlite3 as sq
from fuzzywuzzy import fuzz
from random import choice

import dataupdate

classic = ['классический']
modern = ['современный']
rand = ['девушка', 'женщина', 'пин-ап']
no_repeat = ['a']  # Иногда база возвращает 'а' вместо ссылки, ее наличие в списке не дает произойти ошибке
st = 'style == '
cl = "'classic'"
mod = "'modern'"
aut = 'author =='


def give_pic(string):
    """
    Основная функция, принимает сообщение, выполняет проверку и формирует результат
    """
    ls = message_conversion(str(string))
    if text_check(ls, classic):
        return pic_from_data(st + cl)
    elif text_check(ls, modern):
        return pic_from_data(st + mod)
    elif text_check(ls, rand):
        res = pic_from_data(st + (choice([cl, mod])))
        return res
    else:
        return no_pic()


def message_conversion(string):
    """
    Принимает сообщение, удаляет из него знаки препинания, разбивает на отдельные слова.
    Возвращает список
    """
    et = ['.', ',', '-']
    ls = string
    for x in et:
        ls = ls.replace(x, '')
    ls = ls.split(' ')
    for y in ls:
        if len(y) <= 2:
            ls.remove(y)
    return ls


def text_check(lst, ref, acc=65):
    """
    Проводит проверку на соответствие слов с эталонным списком согласно расстоянию Левенштайна
    """
    ind = False
    for x in lst:
        for y in ref:
            comp = fuzz.ratio(x, y)
            if comp >= acc:
                ind = True
                break
    return ind


def pic_from_data(que):
    """
    Выбирает картинку из классических или современных работ
    либо одного из авторов, если пользователь запросит конкретного и возвращает кортеж с информацией и ссылкой
    """
    res = 'flag'  # res[2] - 'a', гарантированно запускает цикл
    while res[2] in no_repeat:
        with sq.connect('data.db') as con:
            cur = con.cursor()
            cur.execute(f"SELECT * FROM pic WHERE {que} ORDER BY RANDOM() LIMIT 1")
            res = cur.fetchall()[0]
    no_repeat.append(res[2])
    if len(no_repeat) > dataupdate.stack_size['min']:
        del no_repeat[1:(dataupdate.stack_size['min']//2)]
    return res


def no_pic():
    """
    В случае если запрос не распознан возвращает кортеж с текстовым сообщением и False вместо ссылки
    """
    res = ('Чтобы я прислал пин-ап воспользуйтесь кнопками', '', 'no_pic', '')
    return res


def info_from_data(author=None, style=False):
    """
    Возвращает текстовую информацию в зависимости от вызова
    param author: Передается имя автора
    param style: Если False то вернет биографию автора, если True информацию о стиле
    return: Текстовая информация
    """
    if not style:
        with sq.connect('data.db') as con:
            cur = con.cursor()
            cur.execute(f"SELECT bio FROM authors WHERE author == '{author}'")
            res = cur.fetchall()[0]
            return res
    elif style:
        with sq.connect('data.db') as con:
            cur = con.cursor()
            cur.execute(f"SELECT value FROM date")
            res = cur.fetchall()[0]
            return res
