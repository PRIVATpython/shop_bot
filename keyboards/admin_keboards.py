from telebot import types
from db import get_admin_data_no_subcategory, main_category_no_subcategory_data
from db import main_category_subcategory_data, get_category_subcategory


def main_admin_keyboard():
    """Главная админская клавиатура"""
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    add = types.KeyboardButton('Добавить')
    delete = types.KeyboardButton('Удалить')
    chande = types.KeyboardButton('Изменить')
    keyboard.add(add)
    keyboard.add(delete)
    keyboard.add(chande)
    return keyboard


def add_admin_keyboard():
    """Подкатегория/добавить - админская клавиатура"""
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    product = types.KeyboardButton('Добавить аккаунты')
    new_goods = types.KeyboardButton('Добавить новый товар')
    new_cat = types.KeyboardButton('Добавить новую подкатегорию')
    add_main = types.KeyboardButton('Добавить главную категорию')
    back = types.KeyboardButton('Назад')
    keyboard.add(product)
    keyboard.add(new_goods)
    keyboard.add(new_cat)
    keyboard.add(add_main)
    keyboard.add(back)
    return keyboard


def delete_admin_keyboard():
    """Подкатегория/удалить - админская клавиатура"""
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    delete_goods = types.KeyboardButton('Удалить товар')
    delete_cat = types.KeyboardButton('Удалить подкатегорию')
    delete_main = types.KeyboardButton('Удалить главную категорию')
    back = types.KeyboardButton('Назад')
    keyboard.add(delete_goods)
    keyboard.add(delete_cat)
    keyboard.add(delete_main)
    keyboard.add(back)
    return keyboard


def change_admin_keyboard():
    """Подкатегория/изменить - админская клавиатура"""
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    change_goods = types.KeyboardButton('Изменить товар')
    change_cat = types.KeyboardButton('Изменить подкатегорию')
    change_main_cat = types.KeyboardButton('Изменить главную категорию')
    back = types.KeyboardButton('Назад')
    keyboard.add(change_goods)
    keyboard.add(change_cat)
    keyboard.add(change_main_cat)
    keyboard.add(back)
    return keyboard


def admin_product_keyboard(category):
    """Генерит клавиатуру из всех типов(Subcategory - No subcategory)"""
    keyboard = types.InlineKeyboardMarkup()
    with_cat = main_category_subcategory_data()
    no_cat = main_category_no_subcategory_data()
    for item in with_cat:
        keyboard.add(types.InlineKeyboardButton(text=with_cat[item], callback_data=f'{category}|{item}|None'))
    for item in no_cat:
        keyboard.add(types.InlineKeyboardButton(text=no_cat[item], callback_data=f'{category}|{item}|None'))
    return keyboard


def admin_no_subcategory_keboard(category, category_goods):
    """Генерит клавиатуру товаров |No subcategory"""
    keyboard = types.InlineKeyboardMarkup()
    keyboard_data = get_admin_data_no_subcategory(category_goods)
    for item in keyboard_data:
        callback = item['callback'].split('|')
        keyboard.add(types.InlineKeyboardButton(text=item['name'], callback_data=f"{category}|{callback[0]}|{callback[1]}"))
    return keyboard


def admin_category_subcategory_keyboard(cat, category):
    """Генерит клавиатуру подкатегорий |Subcategory"""
    keyboard = types.InlineKeyboardMarkup()
    keyboard_data = get_category_subcategory(cat)
    for item in keyboard_data:
        callback = item['callback'].split('|')
        keyboard.add(types.InlineKeyboardButton(text=item['name'], callback_data=f"{category}|{callback[0]}|{callback[1]}|None"))
    else:
        keyboard.add(types.InlineKeyboardButton(text='Назад', callback_data=f"{category}|{callback[0]}|{callback[1]}|back"))
    return keyboard


def admin_service_subcategory_keyboard(category, service):
    """Генерит клавиатуру товаров |Subcategory"""
    keyboard = types.InlineKeyboardMarkup()
    try:
        for item in service:
            callback = item['callback'].split('|')
            keyboard.add(
                types.InlineKeyboardButton(text=item['name'], callback_data=f"{category}|{callback[0]}|{callback[1]}|{callback[2]}"))
    except:
        pass
    keyboard.add(types.InlineKeyboardButton(text='<< Назад', callback_data=f"{category}|back"))
    return keyboard


def add_category_keyboard(category):
    """Клавитаура для Добавить подкатегорию"""
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
    keyboard.add(types.InlineKeyboardButton(text=f'Изменить описание', callback_data=f"{callback}|description"))
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


def clone_img_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text=f'Взять картинку из подгатегории', callback_data=f"get_subcat_img"))
    keyboard.add(types.InlineKeyboardButton(text=f'Отмена', callback_data=f"cancel_input|None"))
    return keyboard


def generation_account_keyboard(callback):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text=f'Заполнить рандомными аккаунтами => login|password',
                                            callback_data=f"add_acc|{callback}|normal_acc"))
    keyboard.add(types.InlineKeyboardButton(text=f'Заполнить рандомными ключами для игр', callback_data=f"add_acc|{callback}|cd_key"))
    keyboard.add(types.InlineKeyboardButton(text=f'Отмена', callback_data=f"cancel_input|None"))
    return keyboard
