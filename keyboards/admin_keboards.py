from telebot import types
from db import get_admin_data_no_subcategory, main_category_no_subcategory_data
from db import main_category_subcategory_data, get_category_subcategory


def main_admin_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    product = types.KeyboardButton('Добавить аккаунты')
    new_goods = types.KeyboardButton('Добавить новый товар')
    new_cat = types.KeyboardButton('Добавить новую подкатегорию')
    delete_goods = types.KeyboardButton('Удалить товар')
    delete_cat = types.KeyboardButton('Удалить подкатегорию')
    change_cat = types.KeyboardButton('Изменить подкатегорию')
    change_goods = types.KeyboardButton('Изменить товар')
    add_main = types.KeyboardButton('Добавить главную категорию')
    del_main = types.KeyboardButton('Удалить главную категорию')
    keyboard.add(product)
    keyboard.add(new_goods, delete_goods)
    keyboard.add(new_cat, delete_cat)
    keyboard.add(change_cat, change_goods)
    keyboard.add(add_main, del_main)
    return keyboard

def admin_product_keyboard(category):
    keyboard = types.InlineKeyboardMarkup()
    with_cat = main_category_subcategory_data()
    no_cat = main_category_no_subcategory_data()
    for item in with_cat:
        keyboard.add(types.InlineKeyboardButton(text=with_cat[item], callback_data=f'{category}|{item}|None'))
    for item in no_cat:
        keyboard.add(types.InlineKeyboardButton(text=no_cat[item], callback_data=f'{category}|{item}|None'))
    return keyboard

def admin_no_subcategory_keboard(category, category_goods):
    keyboard = types.InlineKeyboardMarkup()
    keyboard_data = get_admin_data_no_subcategory(category_goods)
    for item in keyboard_data:
        callback = item['callback'].split('|')
        keyboard.add(types.InlineKeyboardButton(text=item['name'], callback_data=f"{category}|{callback[0]}|{callback[1]}"))
    return keyboard

def admin_category_subcategory_keyboard(cat, category):
    keyboard = types.InlineKeyboardMarkup()
    keyboard_data = get_category_subcategory(cat)
    for item in keyboard_data:
        callback = item['callback'].split('|')
        keyboard.add(types.InlineKeyboardButton(text=item['name'], callback_data=f"{category}|{callback[0]}|{callback[1]}|None"))
    else:
        keyboard.add(types.InlineKeyboardButton(text='Назад', callback_data=f"{category}|{callback[0]}|{callback[1]}|back"))

    return keyboard

def admin_service_subcategory_keboard(category ,service):
    keyboard = types.InlineKeyboardMarkup()
    try:
        for item in service:
            callback = item['callback'].split('|')
            keyboard.add(types.InlineKeyboardButton(text=item['name'], callback_data=f"{category}|{callback[0]}|{callback[1]}|{callback[2]}"))
    except:
        pass
    keyboard.add(types.InlineKeyboardButton(text='<< Назад', callback_data=f"{category}|back"))
    return keyboard


def add_category_keyboard(category):    # Продолжи от сюда, на стадии админ - добавить категорию
    keyboard = types.InlineKeyboardMarkup()
    with_cat = main_category_subcategory_data()
    for item in with_cat:
        keyboard.add(types.InlineKeyboardButton(text=with_cat[item], callback_data=f'{category}|{item}|None'))
    return keyboard

def del_yes_no(callback):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text=f'Да', callback_data=f"{callback}|yes"))
    keyboard.add(types.InlineKeyboardButton(text=f'Нет', callback_data=f"{callback}|no"))
    return keyboard

def change_img_name(callback):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text=f'Изменить картинку', callback_data=f"{callback}|img"))
    keyboard.add(types.InlineKeyboardButton(text=f'Изменить название', callback_data=f"{callback}|name"))
    return keyboard

def change_img_price_name(callback):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text=f'Изменить картинку', callback_data=f"{callback}|img"))
    keyboard.add(types.InlineKeyboardButton(text=f'Изменить цену', callback_data=f"{callback}|price"))
    keyboard.add(types.InlineKeyboardButton(text=f'Изменить название', callback_data=f"{callback}|name"))
    return keyboard

def cat_or_no_cat(category):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text=f'С подкатегорией', callback_data=f"{category}|with"))
    keyboard.add(types.InlineKeyboardButton(text=f'Без подкатегории', callback_data=f"{category}|without"))
    return keyboard

def cancel_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text=f'Отмена', callback_data=f"cancel_input|None"))
    return keyboard