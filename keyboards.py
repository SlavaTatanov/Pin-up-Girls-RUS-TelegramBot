from telebot import types

keyboards = {}
back_button = types.KeyboardButton('Назад')


def keyboards_create():
    basic_markup_create()
    menu_markup_create()
    admin_markup_create()


def basic_markup_create():
    basic_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    button_1_01 = types.KeyboardButton('Классический пин-ап')
    button_1_02 = types.KeyboardButton('Современный пин-ап')
    button_1_03 = types.KeyboardButton('Меню')
    basic_markup.add(button_1_01, button_1_02)
    basic_markup.add(button_1_03)
    keyboards['basic_markup'] = basic_markup


def menu_markup_create():
    menu_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    button_2_01 = types.KeyboardButton('Классические авторы')
    button_2_02 = types.KeyboardButton('Современные авторы')
    button_2_03 = types.KeyboardButton('О стиле')
    menu_markup.add(button_2_01, button_2_02, button_2_03, back_button, row_width=1)
    keyboards['menu_markup'] = menu_markup


def admin_markup_create():
    admin_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    button_3_01 = types.KeyboardButton('Обновить БД')
    admin_markup.add(button_3_01, back_button, row_width=1)
    keyboards['admin_markup'] = admin_markup


author_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)


def keyboard_create(lst, classic):
    classic_keyboard_buttons = []
    modern_keyboard_buttons = []
    if classic:
        classic_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
        for x in lst:
            classic_keyboard_buttons.append(types.KeyboardButton(str(x)))
        classic_markup.add(*classic_keyboard_buttons, row_width=1)
        classic_markup.add(back_button)
        keyboards['classic_markup'] = classic_markup
    else:
        modern_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
        for x in lst:
            modern_keyboard_buttons.append(types.KeyboardButton(str(x)))
        modern_markup.add(*modern_keyboard_buttons, row_width=1)
        modern_markup.add(back_button)
        keyboards['modern_markup'] = modern_markup


def author_keyboard_create(mess):
    global author_markup
    author_markup = types.ReplyKeyboardRemove
    author_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    author_markup.add(f'Био. {mess}', f'Работы {mess}', back_button, row_width=1)
