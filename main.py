import telebot
import config
import dataupdate
import keyboards
from pic import give_pic

bot = telebot.TeleBot(config.token)

dataupdate.data_upd()  # При старте программы автоматически подхватывает актуальную БД гугл диска и создает/обновляет ее
actual_keyboard = keyboards.menu_markup


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет, если хочешь я отправлю тебе пин-ап', reply_markup=keyboards.basic_markup)


@bot.message_handler(content_types=['text'])
def first(message):
    mess = str.lower(message.text)
    res = give_pic(mess)
    if mess == 'меню':
        bot.send_message(message.chat.id, 'Вызов меню', reply_markup=keyboards.menu_markup)
        bot.register_next_step_handler(message, menu)
    elif mess == 'admin.run':
        bot.send_message(message.chat.id, 'Запуск режима администратора', reply_markup=keyboards.admin_markup)
        bot.register_next_step_handler(message, admin_mod)
    elif not res[2] == 'no_pic':
        bot.send_photo(message.chat.id, res[2], f'{res[0]}\nХуд. {res[1]}\nИсточник {res[3]}',
                       reply_markup=keyboards.basic_markup)
    elif res[2] == 'no_pic':
        bot.send_message(message.chat.id, res[0], reply_markup=keyboards.basic_markup)


def menu(message):
    mess = str.lower(message.text)
    global actual_keyboard
    if mess == 'назад':
        bot.send_message(message.chat.id, 'Возврат', reply_markup=keyboards.basic_markup)
        bot.register_next_step_handler(message, first)
    elif mess == 'современные авторы':
        actual_keyboard = keyboards.modern_markup
        bot.send_message(message.chat.id, 'Список современных авторов', reply_markup=actual_keyboard)
        bot.register_next_step_handler(message, author_menu)
    elif mess == 'классические авторы':
        actual_keyboard = keyboards.classic_markup
        bot.send_message(message.chat.id, 'Список классических авторов', reply_markup=actual_keyboard)
        bot.register_next_step_handler(message, author_menu)
    else:
        bot.send_message(message.chat.id, 'Для возврата нажмите "назад"', reply_markup=keyboards.menu_markup)
        bot.register_next_step_handler(message, menu)


def admin_mod(message):
    mess = message.text
    if mess == 'Обновить БД':
        bot.send_message(message.chat.id, 'Обновляю', reply_markup=keyboards.admin_markup)
        dataupdate.data_upd()
        bot.send_message(message.chat.id, 'Готово', reply_markup=keyboards.admin_markup)
        bot.register_next_step_handler(message, admin_mod)
    elif mess == 'Назад':
        bot.send_message(message.chat.id, 'Возврат', reply_markup=keyboards.basic_markup)
        bot.register_next_step_handler(message, first)


def author_menu(message):
    mess = message.text
    if mess in dataupdate.modern_authors or mess in dataupdate.classic_authors:
        keyboards.author_keyboard_create(mess)
        bot.send_message(message.chat.id, 'О авторе', reply_markup=keyboards.author_markup)
        bot.register_next_step_handler(message, one_author_menu)
    elif mess == 'Назад':
        bot.send_message(message.chat.id, 'Возврат', reply_markup=keyboards.menu_markup)
        bot.register_next_step_handler(message, menu)
    else:
        bot.send_message(message.chat.id, 'Воспользуйтесь кнопками', reply_markup=actual_keyboard)
        bot.register_next_step_handler(message, author_menu)


def one_author_menu(message):
    mess = message.text
    if mess == 'Назад':
        bot.send_message(message.chat.id, 'Возврат', reply_markup=actual_keyboard)
        bot.register_next_step_handler(message, author_menu)
    else:
        bot.send_message(message.chat.id, 'Используйте кнопки', reply_markup=keyboards.author_markup)
        bot.register_next_step_handler(message, one_author_menu)


bot.polling(non_stop=True)
