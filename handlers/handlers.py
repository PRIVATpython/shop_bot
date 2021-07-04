import telebot
from settings import TELEGRAM_KEY
from keyboards import (product_keyboard, category_subcategory_keyboard, subcategory_keyboard, pay_keyboard,
                       account_no_subcategory_keyboard, buy_keyboard, pay_bonus_keyboard)
from db import get_subcategory_data, get_subcategory, give_account_no_subcategory, main_category_subcategory, give_account_subcategory
from db import main_category_no_subcategory, get_data_account_no_subcategory
from db import get_temp_cart
from db import get_bonus, give_bonus
from db import get_or_create_user, set_temp_cart, set_count_temp_cart, set_default_temp_cart


bot = telebot.TeleBot(TELEGRAM_KEY, parse_mode='MARKDOWN')
with_cat = main_category_subcategory()
no_cat = main_category_no_subcategory()


@bot.message_handler(regexp='^(💰 Товары)$')
@bot.callback_query_handler(func=lambda call: call.data.split('|')[0] == 'back' and call.data.split('|')[1] == 'category')
def product(message):
    try:
        user_id = message.chat.id
        global with_cat
        with_cat = main_category_subcategory()
        global no_cat
        no_cat = main_category_no_subcategory()
        set_default_temp_cart(user_id)
        bot.send_message(user_id, 'Выберите категорию: ', reply_markup=product_keyboard())
    except AttributeError:
        set_default_temp_cart(message.message.chat.id)
        bot.delete_message(message.message.chat.id, message.message.message_id)
        bot.send_message(message.message.chat.id, 'Выберите категорию: ', reply_markup=product_keyboard())


@bot.callback_query_handler(func=lambda call: call.data.split('|')[0] in with_cat and call.data.split('|')[1] == 'main')
@bot.callback_query_handler(func=lambda call: call.data.split('|')[0] in with_cat and call.data.split('|')[1] == 'back')
def subcategory_main(call):  # Главная
    """Subcategory - subcategory list"""
    global with_cat
    with_cat = main_category_subcategory()
    user_id = call.message.chat.id
    bot.answer_callback_query(call.id)
    bot.delete_message(user_id, call.message.message_id)
    set_default_temp_cart(user_id)
    bot.send_message(user_id, text='Выберите категорию: ', reply_markup=category_subcategory_keyboard(call.data.split('|')[0]))


@bot.callback_query_handler(func=lambda call: call.data.split('|')[0] in with_cat and call.data.split('|')[3] == 'buy')
def subcategory_buy(call):
    """Subcategory - control count"""
    user_id = call.message.chat.id
    subcategory_data = get_subcategory_data(call.data.split('|')[2])
    set_temp_cart(user_id, subcategory_data, call.data.split('|')[0])
    answer = set_count_temp_cart(user_id, subcategory_data, int(call.data.split('|')[4]), call.data.split('|')[0])
    if answer is False:
        bot.answer_callback_query(call.id, text='Минимальное количество товара: 1 шт')
    elif answer is True:
        user = get_or_create_user(call.message.chat)
        bot.answer_callback_query(call.id, text=f'Максимальное количество товара: {user["temp_cart"]["count"]} шт.')
    return subcategory_data_prod(call)


@bot.callback_query_handler(func=lambda call: call.data.split('|')[0] in with_cat and call.data.split('|')[1] != 'main' and
                                              call.data.split('|')[2] != 'None' and call.data.split('|')[2] != 'back')
def subcategory_data_prod(call):
    """Subcategory - product page"""
    user_id = call.message.chat.id
    subcategory_data = get_subcategory_data(call.data.split('|')[2])
    set_temp_cart(user_id, subcategory_data, call.data.split('|')[0])
    text = subcategory_page(subcategory_data)
    user = get_or_create_user(call.message.chat)
    bot.delete_message(user_id, call.message.message_id)
    photo = subcategory_data['img']
    if photo.split('/')[0] == 'img':
        photo = open(photo, 'rb')
    bot.send_photo(chat_id=user_id, photo=photo, caption=text,
                   reply_markup=buy_keyboard(count=user['temp_cart']['count'],
                                             service=f"{call.data.split('|')[0]}|{call.data.split('|')[1]}|{call.data.split('|')[2]}",
                                             back=f"{call.data.split('|')[0]}|{call.data.split('|')[1]}"))


@bot.callback_query_handler(func=lambda call: call.data.split('|')[0] in with_cat and call.data.split('|')[1] != 'main')
@bot.callback_query_handler(func=lambda call: call.data.split('|')[0] in with_cat and call.data.split('|')[3] == 'back')
def subcategory_product_list(call):
    """Subcategory - product list"""
    user_id = call.message.chat.id
    category = get_subcategory(call.data.split('|')[1])
    bot.answer_callback_query(call.id)
    bot.delete_message(user_id, call.message.message_id)
    photo = category['img']
    if photo.split('/')[0] == 'img':
        photo = open(photo, 'rb')
    bot.send_photo(chat_id=user_id, photo=photo, caption='Выберите аккаунт:',
                   reply_markup=subcategory_keyboard(call.data.split('|')[0], call.data.split('|')[1]))


def subcategory_page(service):
    text = f"""{service['name'].upper()} 
➖➖➖➖➖➖➖➖➖➖➖➖
Цена: {service['price']} рублей

Доступно: {len(service['accounts'])} шт

📃 Описание: {service['description']}
➖➖➖➖➖➖➖➖➖➖➖➖"""
    return text

############################################################################################################################################

@bot.callback_query_handler(func=lambda call: call.data.split('|')[0] in no_cat and call.data.split('|')[1] == 'main')
@bot.callback_query_handler(func=lambda call: call.data.split('|')[0] in no_cat and call.data.split('|')[1] == 'back')
def main_no_subcategory(call):
    """No subcategory - product list"""
    global no_cat
    no_cat = main_category_no_subcategory()
    user_id = call.message.chat.id
    bot.answer_callback_query(call.id)
    bot.delete_message(user_id, call.message.message_id)
    set_default_temp_cart(user_id)
    bot.send_message(user_id, text='Выберите товар: ', reply_markup=account_no_subcategory_keyboard(call.data.split('|')[0]))


@bot.callback_query_handler(func=lambda call: call.data.split('|')[0] in no_cat and call.data.split('|')[2] == 'buy')
def no_subcategory_buy(call):
    """No subcategory - control count"""
    user_id = call.message.chat.id
    callback = call.data.split('|')[1]
    service = get_data_account_no_subcategory(callback)
    count = int(call.data.split('|')[3])
    answer = set_count_temp_cart(user_id, service, count, call.data.split('|')[0])
    if answer is False:
        bot.answer_callback_query(call.id, text='Минимальное количество товара: 1 шт.')
    elif answer is True:
        user = get_or_create_user(call.message.chat)
        bot.answer_callback_query(call.id, text=f'Макисмальное количество товара: {user["temp_cart"]["count"]} шт.')
    return account_no_subcategory(call)


@bot.callback_query_handler(func=lambda call: call.data.split('|')[0] in no_cat and call.data.split('|')[1] != 'main')
def account_no_subcategory(call):
    """No subcategory - product page"""
    user_id = call.message.chat.id
    callback = call.data.split('|')[1]
    service = get_data_account_no_subcategory(callback)
    bot.delete_message(user_id, call.message.message_id)
    user = get_or_create_user(call.message.chat)
    set_temp_cart(user['user_id'], service, call.data.split('|')[0])  # задает имя сервиса во временной коризне
    text = no_subcategory_text(service)
    photo = service['img']
    if photo.split('/')[0] == 'img':
        photo = open(photo, 'rb')
    bot.send_photo(chat_id=call.message.chat.id, photo=photo, caption=text,
                   reply_markup=buy_keyboard(count=user['temp_cart']['count'],
                                             service=f"{call.data.split('|')[0]}|{call.data.split('|')[1]}",
                                             back=call.data.split('|')[0]))


def no_subcategory_text(service):
    text = f"""{service['name'].upper()} PREMIUM
➖➖➖➖➖➖➖➖➖➖➖➖
Цена: {service['price']} рублей

Доступно: {len(service['accounts'])} шт

📃 Описание: {service['description']}
➖➖➖➖➖➖➖➖➖➖➖➖"""
    return text

############################################################################################################################################


@bot.callback_query_handler(func=lambda call: call.data.split('|')[0] == 'pay' and call.data.split('|')[-1] == 'pay')
def pay_test(call):
    """Pay handler - Final pay"""
    user_id = call.message.chat.id
    category = call.data.split('|')[1]
    if category in no_cat:
        accounts = give_account_no_subcategory(user_id)
    elif category in with_cat:
        accounts = give_account_subcategory(user_id)
    accounts = '\n'.join(accounts)
    give_bonus(user_id)
    bot.delete_message(user_id, call.message.message_id)
    bot.send_message(chat_id=user_id, text=f'Спасибо за покупку!\n\n{accounts}')


@bot.callback_query_handler(func=lambda call: call.data.split('|')[0] == 'pay')
def pay_handler(call):
    """Pay handler - main pay page"""
    user_id = call.message.chat.id
    if call.data.split('|')[-1] == 'pay_bonus':
        get_bonus(user_id)
        reply_markup = pay_keyboard(call.data.split('|')[1])
    else:
        reply_markup = pay_bonus_keyboard(call.data.split('|')[1], user_id)
    temp_cart = get_temp_cart(user_id)
    bot.delete_message(user_id, call.message.message_id)
    bot.send_message(chat_id=user_id, text=f'Товар: {temp_cart["product"]}\n\nЦена: {temp_cart["price"]}\n\n'
                                           f'Кол-во: {temp_cart["count"]}\n\nЦена за все: {temp_cart["all_price"]}',
                     reply_markup=reply_markup,
                     parse_mode='HTML')
