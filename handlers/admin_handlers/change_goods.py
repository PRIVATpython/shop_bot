from handlers.handlers import bot
from keyboards import (admin_product_keyboard, admin_no_subcategory_keboard, change_img_price_name,
                       admin_category_subcategory_keyboard, admin_service_subcategory_keyboard, cancel_keyboard)
from db import main_category_subcategory, get_subcategory, change_good_subcategory
from db import main_category_no_subcategory, change_no_subcategory
import requests

with_cat = main_category_subcategory()
no_cat = main_category_no_subcategory()

admin_data = {}


@bot.message_handler(regexp='^(Изменить товар)$')
def change_goods(message):
    global with_cat
    with_cat = main_category_subcategory()
    global no_cat
    no_cat = main_category_no_subcategory()
    user_id = message.chat.id
    category = 'change_goods'
    bot.send_message(chat_id=user_id, text=f'Выберите категорию: ', reply_markup=admin_product_keyboard(category))


@bot.callback_query_handler(func=lambda call: call.data.split('|')[0] == 'change_goods'
                                              and call.data.split('|')[1] in no_cat
                                              and call.data.split('|')[2] == 'None')
def change_online_service(call):
    user_id = call.message.chat.id
    category = call.data.split('|')[0]
    bot.delete_message(user_id, call.message.message_id)
    keyboard = admin_no_subcategory_keboard(category, call.data.split('|')[1])
    bot.send_message(chat_id=user_id, text=f'Выберите какой товар изменить: ', reply_markup=keyboard)


@bot.callback_query_handler(
    func=lambda call: call.data.split('|')[0] == 'change_goods' and call.data.split('|')[1] in no_cat and call.data.split('|')[2] != 'None')
def change_online_service(call):
    global admin_data
    user_id = call.message.chat.id
    admin_data[user_id] = {

            'service': call.data.split('|')[2]

    }
    if call.data.split('|')[-1] == 'img':
        bot.delete_message(user_id, call.message.message_id)
        message = bot.send_message(user_id, f"Введите url картинки или отправтье картинку в чат: ", reply_markup=cancel_keyboard())
        bot.register_next_step_handler(message, change_img_online_service)
        return

    elif call.data.split('|')[-1] == 'name':
        bot.delete_message(user_id, call.message.message_id)
        message = bot.send_message(user_id, f"Введите новое название категории: ", reply_markup=cancel_keyboard())
        bot.register_next_step_handler(message, change_name_online_service)
        return

    elif call.data.split('|')[-1] == 'price':
        bot.delete_message(user_id, call.message.message_id)
        message = bot.send_message(user_id, f"Введите новую цену: ", reply_markup=cancel_keyboard())
        bot.register_next_step_handler(message, change_price_online_service)
        return

    bot.delete_message(user_id, call.message.message_id)
    bot.send_message(user_id, f"Выберите что изменить",
                     reply_markup=change_img_price_name(call.data))


def change_img_online_service(message):
    user_id = message.chat.id
    try:
        global admin_data
        if message.text is not None:
            url_photo = message.text
        elif message.photo is not None:
            file_info = bot.get_file(message.photo[-1].file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            filepath = 'img/'
            url_photo = filepath + message.photo[0].file_id + '.jpg'
            with open(url_photo, 'wb') as new_file:
                new_file.write(downloaded_file)
            admin_data[user_id]['img'] = url_photo
        else:
            message = bot.send_message(user_id, f"Введите url картинки или отправтье картинку в чат (Ссылка - текстом, либо картинка): ", reply_markup=cancel_keyboard())
            bot.register_next_step_handler(message, change_img_online_service)
            return
        category = 'img'
        change_no_subcategory(data=url_photo, service=admin_data[user_id]['service'], category=category)
        bot.send_message(user_id, 'Успешно')
        admin_data[user_id] = None
    except:
        message = bot.send_message(user_id, f"Введите url картинки или отправтье картинку в чат (Ссылка - текстом, либо картинка): ", reply_markup=cancel_keyboard())
        bot.register_next_step_handler(message, change_img_online_service)
        return


def change_name_online_service(message):
    user_id = message.chat.id
    try:
        global admin_data
        if message.text is not None:
            name = message.text
            category = 'name'
            change_no_subcategory(data=name, category=category, service=admin_data[user_id]['service'])
            bot.send_message(user_id, 'Успешно')
            admin_data[user_id] = None
        else:
            message = bot.send_message(user_id, f"Введите новое название категории (Только текст) : ", reply_markup=cancel_keyboard())
            bot.register_next_step_handler(message, change_name_online_service)
    except:
        message = bot.send_message(user_id, f"Введите новое название категории (Только текст) : ", reply_markup=cancel_keyboard())
        bot.register_next_step_handler(message, change_name_online_service)

def change_price_online_service(message):
    user_id = message.chat.id
    try:
        global admin_data
        if message.text is not None:
            price = int(message.text)
            category = 'price'
            change_no_subcategory(data=price, category=category, service=admin_data[user_id]['service'])
            bot.send_message(user_id, 'Успешно')
            admin_data[user_id] = None
        else:
            message = bot.send_message(user_id, f"Введите новую цену (Только цифры): ", reply_markup=cancel_keyboard())
            bot.register_next_step_handler(message, change_price_online_service)
    except:
        message = bot.send_message(user_id, f"Введите новую цену (Только цифры): ", reply_markup=cancel_keyboard())
        bot.register_next_step_handler(message, change_price_online_service)

@bot.callback_query_handler(
    func=lambda call: call.data.split('|')[0] == 'change_goods' and call.data.split('|')[1] in with_cat and call.data.split('|')[
        2] == 'None')
def change_social_service(call):
    user_id = call.message.chat.id
    category = call.data.split('|')[0]
    bot.delete_message(user_id, call.message.message_id)
    keyboard = admin_category_subcategory_keyboard(call.data.split('|')[1], category)
    bot.send_message(chat_id=user_id, text=f'Выберите категорию: ', reply_markup=keyboard)


@bot.callback_query_handler(
    func=lambda call: call.data.split('|')[0] == 'change_goods' and call.data.split('|')[1] in with_cat
                                                                and call.data.split('|')[-1] == 'None')
def change_social_service(call):
    user_id = call.message.chat.id
    category = call.data.split('|')[2]
    service = get_subcategory(category)
    keyboard = admin_service_subcategory_keyboard(call.data.split('|')[0], service['accounts_data'])
    bot.delete_message(user_id, call.message.message_id)
    bot.send_message(chat_id=user_id, text=f'Выберите аккаунт: ', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data.split('|')[0] == 'change_goods' and call.data.split('|')[1] in with_cat)
def change_social_service(call):
    global admin_data
    user_id = call.message.chat.id
    admin_data[user_id] = {

            'service': call.data.split('|')[3]

    }
    if call.data.split('|')[-1] == 'img':
        bot.delete_message(user_id, call.message.message_id)
        message = bot.send_message(user_id, f"Введите url картинки или отправтье картинку в чат: ", reply_markup=cancel_keyboard())
        bot.register_next_step_handler(message, change_img_social_service)
        return

    elif call.data.split('|')[-1] == 'name':
        bot.delete_message(user_id, call.message.message_id)
        message = bot.send_message(user_id, f"Введите новое название категории: ", reply_markup=cancel_keyboard())
        bot.register_next_step_handler(message, change_name_social_service)
        return

    elif call.data.split('|')[-1] == 'price':
        bot.delete_message(user_id, call.message.message_id)
        message = bot.send_message(user_id, f"Введите новую цену: ", reply_markup=cancel_keyboard())
        bot.register_next_step_handler(message, change_price_social_service)
        return

    bot.delete_message(user_id, call.message.message_id)
    bot.send_message(user_id, f"Выберите что изменить",
                     reply_markup=change_img_price_name(call.data))


def change_img_social_service(message):
    user_id = message.chat.id
    try:
        global admin_data
        if message.text is not None:
            url_photo = message.text
            if url_photo.split(':')[0] != 'https':
                message = bot.send_message(user_id, f"Url должен начинаться с https:// ", reply_markup=cancel_keyboard())
                bot.register_next_step_handler(message, change_img_social_service)
                return
            if requests.get(url_photo).headers['Content-Type'].split('/')[0] != 'image':
                message = bot.send_message(user_id, f"Введите корректный url картинки: ", reply_markup=cancel_keyboard())
                bot.register_next_step_handler(message, change_img_social_service)
                return
        elif message.photo is not None:
            file_info = bot.get_file(message.photo[-1].file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            filepath = 'img/'
            url_photo = filepath + message.photo[0].file_id + '.jpg'
            with open(url_photo, 'wb') as new_file:
                new_file.write(downloaded_file)
            admin_data[user_id]['img'] = url_photo
        else:
            message = bot.send_message(user_id, f"Введите url картинки или отправтье картинку в чат (Только текст либо только картинку): ", reply_markup=cancel_keyboard())
            bot.register_next_step_handler(message, change_img_social_service)
            return

        category = 'img'
        change_good_subcategory(data=url_photo, service=admin_data[user_id]['service'], category=category)
        bot.send_message(user_id, 'Успешно')
        admin_data[user_id] = None
    except:
        message = bot.send_message(user_id, f"Введите url картинки или отправтье картинку в чат (Только текст либо только картинку): ",
                                   reply_markup=cancel_keyboard())
        bot.register_next_step_handler(message, change_img_social_service)


def change_name_social_service(message):
    user_id = message.chat.id
    try:
        global admin_data
        if message.text is not None:
            name = message.text
            category = 'name'
            change_good_subcategory(data=name, category=category, service=admin_data[user_id]['service'])
            bot.send_message(user_id, 'Успешно')
            admin_data[user_id] = None
        else:
            message = bot.send_message(user_id, f"Введите новое название категории (Только текст): ", reply_markup=cancel_keyboard())
            bot.register_next_step_handler(message, change_name_social_service)
    except:
        message = bot.send_message(user_id, f"Введите новое название категории (Только текст): ", reply_markup=cancel_keyboard())
        bot.register_next_step_handler(message, change_name_social_service)

def change_price_social_service(message):
    user_id = message.chat.id
    global admin_data
    try:
        if message.text is not None:
            price = int(message.text)
            category = 'price'
            change_good_subcategory(data=price, category=category, service=admin_data[user_id]['service'])
            bot.send_message(user_id, 'Успешно')
            admin_data[user_id] = None
        else:
            message = bot.send_message(user_id, f"Введите новую цену (Только цифры): ", reply_markup=cancel_keyboard())
            bot.register_next_step_handler(message, change_price_social_service)
    except:
        message = bot.send_message(user_id, f"Введите новую цену (Только цифры): ", reply_markup=cancel_keyboard())
        bot.register_next_step_handler(message, change_price_social_service)