from telebot import types


basic_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
button1 = types.KeyboardButton('Классический пин-ап')
button2 = types.KeyboardButton('Современный пин-ап')
button3 = types.KeyboardButton('Меню')
basic_markup.add(button1, button2)
basic_markup.add(button3)


menu_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
button4 = types.KeyboardButton('Классические авторы')
button5 = types.KeyboardButton('Современные авторы')
button6 = types.KeyboardButton('О стиле')
button7 = types.KeyboardButton('Назад')
menu_markup.add(button4)
menu_markup.add(button5)
menu_markup.add(button6)
menu_markup.add(button7)
