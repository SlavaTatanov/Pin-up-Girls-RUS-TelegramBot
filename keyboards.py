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


classic_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)

modern_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)

author_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)


def keyboard_create(lst, classic):
    global classic_markup
    global modern_markup
    classic_keyboard_buttons = []
    modern_keyboard_buttons = []
    if classic:
        classic_markup = types.ReplyKeyboardRemove
        classic_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
        for x in lst:
            classic_keyboard_buttons.append(types.KeyboardButton(str(x)))
        classic_markup.add(*classic_keyboard_buttons, row_width=1)
        classic_markup.add(button_2_04)
    else:
        modern_markup = types.ReplyKeyboardRemove
        modern_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
        for x in lst:
            modern_keyboard_buttons.append(types.KeyboardButton(str(x)))
        modern_markup.add(*modern_keyboard_buttons, row_width=1)
        modern_markup.add(button_2_04)


def author_keyboard_create(mess):
    global author_markup
    author_markup = types.ReplyKeyboardRemove
    author_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    author_markup.add(f'Био. {mess}', f'Работы {mess}', button_2_04, row_width=1)
