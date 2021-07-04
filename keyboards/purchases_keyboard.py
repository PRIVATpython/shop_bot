from telebot import types
from db import purch_product


def purch_product_keyboard(user_id):
    keyboard = types.InlineKeyboardMarkup()
    purch_goods = purch_product(user_id)
    for item in purch_goods:
        keyboard.add(types.InlineKeyboardButton(text=item, callback_data=f'{purch_goods[item]}'))
    return keyboard
