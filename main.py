import telebot
import config
import dataupdate
import keyboards
import pic
from pic import give_pic
from tools.admin import admin
from tools.counter import Counter

bot = telebot.TeleBot(config.token)

dataupdate.data_upd()  # При старте программы автоматически подхватывает актуальную БД гугл диска и создает/обновляет ее
actual_keyboard = {}  # Переносит клавиатуру пользователя из функции в функцию и
# сохраняет в словарь
keyboard_this_user = {}  # В этот словарь сохраняется клавиатура пользователя, позволяет двум пользователям иметь свои
# клавиатуры
counter = Counter()


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет, если хочешь я отправлю тебе пин-ап',
                     reply_markup=keyboards.keyboards['basic_markup'])


@bot.message_handler(content_types=['text'])
def first(message):
    mess = str.lower(message.text)
    res = give_pic(mess)
    if mess == 'меню':
        bot.send_message(message.chat.id, 'Вызов меню', reply_markup=keyboards.keyboards['menu_markup'])
        bot.register_next_step_handler(message, menu)
    elif mess == 'admin.run':
        if admin(message.chat.id):
            bot.send_message(message.chat.id, 'Запуск режима администратора',
                             reply_markup=keyboards.keyboards['admin_markup'])
            bot.register_next_step_handler(message, admin_mod)
        else:
            bot.send_message(message.chat.id, 'Доступ запрещен',
                             reply_markup=keyboards.keyboards['basic_markup'])
    elif not res[2] == 'no_pic':
        if not admin(message.chat.id):
            counter.add_id(message.chat.id)
        bot.send_photo(message.chat.id, res[2], f'{res[0]}\nХуд. {res[1]}\nИсточник {res[3]}',
                       reply_markup=keyboards.keyboards['basic_markup'])
    elif res[2] == 'no_pic':
        bot.send_message(message.chat.id, res[0], reply_markup=keyboards.keyboards['basic_markup'])


def menu(message):
    mess = str.lower(message.text)
    user = message.from_user.id
    if mess == 'назад':
        bot.send_message(message.chat.id, 'Возврат', reply_markup=keyboards.keyboards['basic_markup'])
        bot.register_next_step_handler(message, first)
    elif mess == 'современные авторы':
        actual_keyboard[user] = keyboards.keyboards['modern_markup']
        bot.send_message(message.chat.id, 'Список современных авторов', reply_markup=actual_keyboard[user])
        bot.register_next_step_handler(message, author_menu)
    elif mess == 'классические авторы':
        actual_keyboard[user] = keyboards.keyboards['classic_markup']
        bot.send_message(message.chat.id, 'Список классических авторов', reply_markup=actual_keyboard[user])
        bot.register_next_step_handler(message, author_menu)
    elif mess == 'о стиле':
        res = pic.info_from_data(style=True)
        bot.send_message(message.chat.id, res[0], reply_markup=keyboards.keyboards['menu_markup'])
        bot.register_next_step_handler(message, menu)
    else:
        bot.send_message(message.chat.id, 'Для возврата нажмите "назад"',
                         reply_markup=keyboards.keyboards['menu_markup'])
        bot.register_next_step_handler(message, menu)


def admin_mod(message):
    mess = message.text
    if mess == 'Обновить БД':
        bot.send_message(message.chat.id, 'Обновляю', reply_markup=keyboards.keyboards['admin_markup'])
        dataupdate.data_upd()
        bot.send_message(message.chat.id, 'Готово', reply_markup=keyboards.keyboards['admin_markup'])
        bot.register_next_step_handler(message, admin_mod)
    elif mess == 'Счетчик пользователей':
        bot.send_message(message.chat.id, counter.user_count(), reply_markup=keyboards.keyboards['admin_markup'])
        bot.register_next_step_handler(message, admin_mod)
    elif mess == 'Назад':
        bot.send_message(message.chat.id, 'Возврат', reply_markup=keyboards.keyboards['basic_markup'])
        bot.register_next_step_handler(message, first)


def author_menu(message):
    mess = message.text
    user = message.from_user.id
    if mess in dataupdate.modern_authors or mess in dataupdate.classic_authors:
        keyboards.author_keyboard_create(mess)
        keyboard_this_user[user] = keyboards.keyboards['author_markup']
        bot.send_message(message.chat.id, 'О авторе', reply_markup=keyboard_this_user[user])
        bot.register_next_step_handler(message, one_author_menu)
    elif mess == 'Назад':
        del actual_keyboard[user]
        bot.send_message(message.chat.id, 'Возврат', reply_markup=keyboards.keyboards['menu_markup'])
        bot.register_next_step_handler(message, menu)
    else:
        bot.send_message(message.chat.id, 'Воспользуйтесь кнопками', reply_markup=actual_keyboard[user])
        bot.register_next_step_handler(message, author_menu)


def one_author_menu(message):
    user = message.from_user.id
    mess = message.text
    if mess == 'Назад':
        del keyboard_this_user[user]
        bot.send_message(message.chat.id, 'Возврат', reply_markup=actual_keyboard[user])
        bot.register_next_step_handler(message, author_menu)
    elif 'Био.' in mess:
        res = pic.info_from_data(author=mess[5:])
        bot.send_message(message.chat.id, res[0], reply_markup=keyboard_this_user[user])
        bot.register_next_step_handler(message, one_author_menu)
    elif 'Работы' in mess:
        if not admin(message.chat.id):
            counter.add_id(message.chat.id)
        res = pic.pic_from_data(f'{pic.aut} "{mess[7:]}"')
        bot.send_photo(message.chat.id, res[2], f'{res[0]}\nХуд. {res[1]}\nИсточник {res[3]}',
                       reply_markup=keyboard_this_user[user])
        bot.register_next_step_handler(message, one_author_menu)
    else:
        bot.send_message(message.chat.id, 'Используйте кнопки', reply_markup=keyboard_this_user[user])
        bot.register_next_step_handler(message, one_author_menu)


bot.polling(non_stop=True)
