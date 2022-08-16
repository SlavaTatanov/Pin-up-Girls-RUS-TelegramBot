from telebot import types


basic_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
button_1_01 = types.KeyboardButton('Классический пин-ап')
button_1_02 = types.KeyboardButton('Современный пин-ап')
button_1_03 = types.KeyboardButton('Меню')
basic_markup.add(button_1_01, button_1_02)
basic_markup.add(button_1_03)


menu_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
button_2_01 = types.KeyboardButton('Классические авторы')
button_2_02 = types.KeyboardButton('Современные авторы')
button_2_03 = types.KeyboardButton('О стиле')
button_2_04 = types.KeyboardButton('Назад')
menu_markup.add(button_2_01)
menu_markup.add(button_2_02)
menu_markup.add(button_2_03)
menu_markup.add(button_2_04)


admin_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
button_3_01 = types.KeyboardButton('Обновить БД')
admin_markup.add(button_3_01)
admin_markup.add(button_2_04)
