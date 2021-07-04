from telebot import types


def main_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    product = types.KeyboardButton('💰 Товары')
    my_cabinet = types.KeyboardButton('⚙ Мой кабинет')
    my_cart = types.KeyboardButton('🛍 Мои покупки')
    support = types.KeyboardButton('👨‍💻 Тех. поддержка')
    games = types.KeyboardButton('Игры')
    keyboard.add(product, my_cabinet)
    keyboard.add(my_cart, support)
    keyboard.add(games)
    return keyboard
