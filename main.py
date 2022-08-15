import telebot
import config
import dataupdate
import keyboards
from pic import give_pic

bot = telebot.TeleBot(config.token)

dataupdate.data_upd()  # При старте программы автоматически подхватывает актуальную БД гугл диска и создает/обновляет ее


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет, если хочешь я отправлю тебе пин-ап', reply_markup=keyboards.basic_markup)


@bot.message_handler(content_types=['text'])
def first(message):
    mess = str.lower(message.text)
    res = give_pic(mess)
    if mess == 'меню':
        bot.send_message(message.chat.id, 'Вызов меню', reply_markup=keyboards.menu_markup)
        bot.register_next_step_handler(message, two)
    elif not res[2] == 'no_pic':
        bot.send_photo(message.chat.id, res[2], f'{res[0]}\nХуд. {res[1]}\nИсточник {res[3]}',
                       reply_markup=keyboards.basic_markup)
    elif res[2] == 'no_pic':
        bot.send_message(message.chat.id, res[0], reply_markup=keyboards.basic_markup)


def two(message):
    mess = str.lower(message.text)
    if mess == 'назад':
        bot.send_message(message.chat.id, 'Возврат', reply_markup=keyboards.basic_markup)
        bot.register_next_step_handler(message, first)
    elif mess == 'современные авторы':
        bot.send_message(message.chat.id, 'Здесь будут современные авторы')
        bot.register_next_step_handler(message, two)
    elif mess == 'классические авторы':
        bot.send_message(message.chat.id, 'Здесь будут классические авторы')
        bot.register_next_step_handler(message, two)
    else:
        bot.send_message(message.chat.id, 'Для возврата нажмите "назад"', reply_markup=keyboards.menu_markup)
        bot.register_next_step_handler(message, two)


bot.polling(non_stop=True)
