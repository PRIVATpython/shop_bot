from telebot import types


def main_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    product = types.KeyboardButton('💰 Товары')
    my_cabinet = types.KeyboardButton('⚙ Мои баллы')
    my_cart = types.KeyboardButton('🛍 Мои покупки')
    support = types.KeyboardButton('👨‍💻 Тех. поддержка')
    keyboard.add(product, my_cabinet)
    keyboard.add(my_cart, support)
    return keyboard
