from telebot import types
from db import get_data_account_no_subcategory_keyboard, main_category_no_subcategory_data
from db import get_category_subcategory, get_subcategory, main_category_subcategory_data
from db import get_user


def product_keyboard():
    """Генерит клавиатуры главных катеогрий 2ух типов"""
    keyboard = types.InlineKeyboardMarkup()
    with_cat = main_category_subcategory_data()
    no_cat = main_category_no_subcategory_data()
    for item in with_cat:
        keyboard.add(types.InlineKeyboardButton(text=with_cat[item], callback_data=f'{item}|main|None|None|None'))
    for item in no_cat:
        keyboard.add(types.InlineKeyboardButton(text=no_cat[item], callback_data=f'{item}|main|None|None|None'))
    return keyboard


def account_no_subcategory_keyboard(category):
    '''Генерит клавиатуру для товаров No subcategory'''
    keyboard = types.InlineKeyboardMarkup()
    keyboard_data = get_data_account_no_subcategory_keyboard(category)
    for item in keyboard_data:
        keyboard.add(types.InlineKeyboardButton(text=item['name'], callback_data=item['callback']))
    back = types.InlineKeyboardButton(text='<< Назад', callback_data='back|category')
    keyboard.add(back)
    return keyboard


def buy_keyboard(service, count, back):
    '''Клавиатура покупки'''
    keyboard = types.InlineKeyboardMarkup()
    down_1 = types.InlineKeyboardButton(text=f'🔻', callback_data=f'{service}|buy|-1')
    count = types.InlineKeyboardButton(text=f'{count} шт', callback_data=f'{service}|buy|0')
    up_1 = types.InlineKeyboardButton(text=f'🔺', callback_data=f'{service}|buy|1')
    down_10 = types.InlineKeyboardButton(text=f'10 🔻', callback_data=f'{service}|buy|-10')
    up_10 = types.InlineKeyboardButton(text=f'10 🔺', callback_data=f'{service}|buy|10')
    buy = types.InlineKeyboardButton(text=f'Купить', callback_data=f'pay|{back}|None|None')
    back_button = types.InlineKeyboardButton(text='<< Назад', callback_data=f'{back}|back|None|None')
    keyboard.add(down_1, count, up_1)
    keyboard.add(down_10, up_10)
    keyboard.add(buy)
    keyboard.add(back_button)
    return keyboard


def category_subcategory_keyboard(cat):
    '''Генерит клавиатуру для подкатегорий'''
    keyboard = types.InlineKeyboardMarkup()
    category = get_category_subcategory(cat)
    for item in category:
        keyboard.add(types.InlineKeyboardButton(text=item['name'], callback_data=item['callback']))
    keyboard.add(types.InlineKeyboardButton(text='<< Назад', callback_data='back|category'))
    return keyboard


def subcategory_keyboard(cat, category_acc):
    '''Генерит клавитуру для товаров Subcategory'''
    keyboard = types.InlineKeyboardMarkup()
    category = get_subcategory(category_acc)
    category = category['accounts_data']
    for item in category:
        if len(item['accounts']) == 0:
            continue
        keyboard.add(types.InlineKeyboardButton(text=item['name'], callback_data=item['callback']))
    keyboard.add(types.InlineKeyboardButton(text='<< Назад', callback_data=f'{cat}|back|None|None|None'))
    return keyboard


def pay_bonus_keyboard(category, user_id):
    keyboard = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton(text='Оплатить', callback_data=f'pay|{category}|pay')
    qiwi = types.InlineKeyboardButton(text='QIWI', callback_data=f'pay|{category}|qiwi')
    data_user = get_user(user_id=user_id)
    if data_user['temp_cart']['bonus'] > 0:
        buy_bonus = types.InlineKeyboardButton(text=f'Использовать бонусы ({data_user["temp_cart"]["bonus"]} бонусов)',
                                               callback_data=f'pay|{category}|pay_bonus')
        keyboard.add(buy_bonus)
    keyboard.add(button)
    keyboard.add(qiwi)
    return keyboard


def pay_keyboard(category):
    keyboard = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton(text='Оплатить', callback_data=f'pay|{category}|pay')
    qiwi = types.InlineKeyboardButton(text='QIWI', callback_data=f'pay|{category}|qiwi')
    keyboard.add(button)
    keyboard.add(qiwi)
    return keyboard

def check_keyboard(category, pay_service):
    keyboard = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton(text='Проверить оплату', callback_data=f'pay_check|{category}|{pay_service}')
    keyboard.add(button)
    return keyboard
