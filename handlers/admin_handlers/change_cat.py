from handlers.handlers import bot
from keyboards import add_category_keyboard, admin_category_subcategory_keyboard, change_img_name, cancel_keyboard
from db import change_cat_subcategory
import requests
admin_data = {}


@bot.message_handler(regexp='^(Изменить подкатегорию)$')
def add_account_category(message):
    user_id = message.chat.id
    category = 'change_cat'
    bot.send_message(chat_id=user_id, text=f'Выберите категорию: ', reply_markup=add_category_keyboard(category))


@bot.callback_query_handler(func=lambda call: call.data.split('|')[0] == 'change_cat' and call.data.split('|')[2] == 'None')
def change_cat_social(call):
    user_id = call.message.chat.id
    admin = call.data.split('|')[0]
    category = call.data.split('|')[1]
    bot.delete_message(user_id, call.message.message_id)
    bot.send_message(user_id, f"Выберите категорию для изменения: ", reply_markup=admin_category_subcategory_keyboard(category, admin))


@bot.callback_query_handler(func=lambda call: call.data.split('|')[0] == 'change_cat' and call.data.split('|')[2] != 'None')
def change_cat(call):
    global admin_data
    user_id = call.message.chat.id
    admin_data = {

            'service': call.data.split('|')[2]

    }
    if call.data.split('|')[-1] == 'img':
        bot.delete_message(user_id, call.message.message_id)
        message = bot.send_message(user_id, f"Введите url картинки: ", reply_markup=cancel_keyboard())
        bot.register_next_step_handler(message, change_img)
        return
    elif call.data.split('|')[-1] == 'name':
        bot.delete_message(user_id, call.message.message_id)
        message = bot.send_message(user_id, f"Введите новое название категории: ", reply_markup=cancel_keyboard())
        bot.register_next_step_handler(message, change_name)
        return
    bot.delete_message(user_id, call.message.message_id)
    bot.send_message(user_id, f"Выберите что изменить",
                     reply_markup=change_img_name(call.data))


def change_img(message):
    user_id = message.chat.id
    try:
        global admin_data
        if message.text is not None:
            url_photo = message.text
            if url_photo.split(':')[0] != 'https':
                message = bot.send_message(user_id, f"Url должен начинаться с https:// ", reply_markup=cancel_keyboard())
                bot.register_next_step_handler(message, change_img)
                return
            if requests.get(url_photo).headers['Content-Type'].split('/')[0] != 'image':
                message = bot.send_message(user_id, f"Введите корректный url картинки: ", reply_markup=cancel_keyboard())
                bot.register_next_step_handler(message, change_img)
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
            message = bot.send_message(user_id, f"Введите url картинки или отправтье картинку в чат (Только текст или только картинка): ", reply_markup=cancel_keyboard())
            bot.register_next_step_handler(message, change_img)
            return
        category = 'img'
        change_cat_subcategory(url_photo=url_photo, category=category, service=admin_data[user_id]['service'])
        bot.send_message(user_id, 'Успешно')
        admin_data[user_id] = None
    except:
        message = bot.send_message(user_id, f"Введите url картинки или отправтье картинку в чат (Только текст или только картинка): ",
                                   reply_markup=cancel_keyboard())
        bot.register_next_step_handler(message, change_img)


def change_name(message):
    user_id = message.chat.id
    try:
        global admin_data
        if message.text is not None:
            name = message.text
            category = 'name'
            change_cat_subcategory(url_photo=name, category=category, service=admin_data[user_id]['service'])
            bot.send_message(user_id, 'Успешно')
            admin_data[user_id] = None
            return
        else:
            message = bot.send_message(user_id, f"Введите новое название категории (Только текст): ", reply_markup=cancel_keyboard())
            bot.register_next_step_handler(message, change_name)
            return
    except:
        message = bot.send_message(user_id, f"Введите новое название категории (Только текст): ", reply_markup=cancel_keyboard())
        bot.register_next_step_handler(message, change_name)