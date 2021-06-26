from handlers.handlers import bot
from keyboards import cat_or_no_cat, cancel_keyboard
from utilites import generate_alphanum_random_string
from db import add_new_cat_subcategory, add_new_no_subcategory
import requests

admin_data = {}


@bot.message_handler(regexp='^(Добавить главную категорию)$')
def add_account_category(message):
    user_id = message.chat.id
    category = 'add_main'
    # bot.delete_message(user_id, call.message.message_id)
    bot.send_message(chat_id=user_id, text=f'Выберите категорию: ', reply_markup=cat_or_no_cat(category))


@bot.callback_query_handler(func=lambda call: call.data.split('|')[0] == 'add_main' and call.data.split('|')[1] == 'with')
def with_cat(call):
    user_id = call.message.chat.id
    bot.delete_message(user_id, call.message.message_id)
    message = bot.send_message(chat_id=user_id, text=f'Что бы добавить новую категорию, добавтье хотя бы 1 подкатегорию\n'
                                                     f'Введите название главной категории: ', reply_markup=cancel_keyboard())
    bot.register_next_step_handler(message, name_main_cat)


def name_main_cat(message):
    user_id = message.chat.id
    try:
        global admin_data
        if message.text is not None:
            name_cat = message.text
            high_id = generate_alphanum_random_string(6)
            admin_data[user_id] = {

                    'high_id': high_id,
                    'name_category': name_cat

            }
            message = bot.send_message(chat_id=user_id, text=f'Введите название подкатегории:', reply_markup=cancel_keyboard())
            bot.register_next_step_handler(message, name_subcategory)
        else:
            message = bot.send_message(chat_id=user_id, text=f'Что бы добавить новую категорию, добавтье хотя бы 1 подкатегорию\n'
                                                             f'Введите название главной категории: ', reply_markup=cancel_keyboard())
            bot.register_next_step_handler(message, name_main_cat)
    except:
        message = bot.send_message(chat_id=user_id, text=f'Что бы добавить новую категорию, добавтье хотя бы 1 подкатегорию\n'
                                                         f'Введите название главной категории: ', reply_markup=cancel_keyboard())
        bot.register_next_step_handler(message, name_main_cat)

def name_subcategory(message):
    user_id = message.chat.id
    try:
        global admin_data
        if message.text is not None:
            subcategory_name = message.text
            admin_data[user_id]['name'] = subcategory_name
            message = bot.send_message(chat_id=user_id, text=f'Введите url картинки или отправтье картинку в чат:', reply_markup=cancel_keyboard())
            bot.register_next_step_handler(message, url_subcategory)
        else:
            message = bot.send_message(chat_id=user_id, text=f'Введите название подкатегории:', reply_markup=cancel_keyboard())
            bot.register_next_step_handler(message, name_subcategory)
    except:
        message = bot.send_message(chat_id=user_id, text=f'Введите название подкатегории:', reply_markup=cancel_keyboard())
        bot.register_next_step_handler(message, name_subcategory)

def url_subcategory(message):
    user_id = message.chat.id
    try:
        global admin_data
        if message.text is not None:
            url_photo = message.text
            if url_photo.split(':')[0] != 'https':
                message = bot.send_message(user_id, f"Url должен начинаться с https:// ", reply_markup=cancel_keyboard())
                bot.register_next_step_handler(message, url_no_subcategory_photo)
                return
            if requests.get(url_photo).headers['Content-Type'].split('/')[0] != 'image':
                message = bot.send_message(user_id, f"Введите корректный url картинки: ", reply_markup=cancel_keyboard())
                bot.register_next_step_handler(message, url_no_subcategory_photo)
                return
            admin_data[user_id]['img'] = url_photo
        elif message.photo is not None:
            file_info = bot.get_file(message.photo[-1].file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            filepath = 'img/'
            url = filepath + message.photo[0].file_id + '.jpg'
            with open(url, 'wb') as new_file:
                new_file.write(downloaded_file)
            admin_data[user_id]['img'] = url
        else:
            message = bot.send_message(chat_id=user_id, text=f'Введите url картинки или отправтье картинку в чат:', reply_markup=cancel_keyboard())
            bot.register_next_step_handler(message, url_subcategory)
            return
    except:
        message = bot.send_message(chat_id=user_id, text=f'Введите url картинки или отправтье картинку в чат:',
                                   reply_markup=cancel_keyboard())
        bot.register_next_step_handler(message, url_subcategory)

        # Закончил здесь
    add_new_cat_subcategory(admin_data[user_id])
    admin_data[user_id] = None
    bot.send_message(user_id, 'Успешно')


@bot.callback_query_handler(func=lambda call: call.data.split('|')[0] == 'add_main' and call.data.split('|')[1] == 'without')
def with_cat(call):
    user_id = call.message.chat.id
    bot.delete_message(user_id, call.message.message_id)
    message = bot.send_message(chat_id=user_id, text=f'Что бы добавить новую категорию, добавтье хотя бы 1 товар\n'
                                                     f'Введите название главной категории: ', reply_markup=cancel_keyboard())
    bot.register_next_step_handler(message, name_no_subcategory)


def name_no_subcategory(message):
    user_id = message.chat.id
    try:
        global admin_data

        if message.text is not None:
            name_cat = message.text
            high_id = generate_alphanum_random_string(6)

            admin_data[user_id] = {

                    'high_id': high_id,
                    'name_category': name_cat

            }
            message = bot.send_message(chat_id=user_id, text=f'Введите название товара:', reply_markup=cancel_keyboard())
            bot.register_next_step_handler(message, name_no_subcategory_goods)
            return
        else:
            message = bot.send_message(chat_id=user_id, text=f'Что бы добавить новую категорию, добавтье хотя бы 1 товар\n'
                                                             f'Введите название главной категории: ', reply_markup=cancel_keyboard())
            bot.register_next_step_handler(message, name_no_subcategory)
    except:
        message = bot.send_message(chat_id=user_id, text=f'Что бы добавить новую категорию, добавтье хотя бы 1 товар\n'
                                                         f'Введите название главной категории: ', reply_markup=cancel_keyboard())
        bot.register_next_step_handler(message, name_no_subcategory)

def name_no_subcategory_goods(message):
    global admin_data
    user_id = message.chat.id
    try:
        if message.text is not None:
            name_subcat = message.text
            admin_data[user_id]['name'] = name_subcat
            message = bot.send_message(chat_id=user_id, text=f'Введите цену:', reply_markup=cancel_keyboard())
            bot.register_next_step_handler(message, no_subcategory_price)
            return
        else:
            message = bot.send_message(chat_id=user_id, text=f'Введите название товара:', reply_markup=cancel_keyboard())
            bot.register_next_step_handler(message, name_no_subcategory_goods)
    except:
        message = bot.send_message(chat_id=user_id, text=f'Введите название товара:', reply_markup=cancel_keyboard())
        bot.register_next_step_handler(message, name_no_subcategory_goods)

def no_subcategory_price(message):
    user_id = message.chat.id
    try:
        global admin_data

        if message.text is not None:
            try:
                price = int(message.text)
            except:
                message = bot.send_message(chat_id=user_id, text=f'Введите цену:', reply_markup=cancel_keyboard())
                bot.register_next_step_handler(message, no_subcategory_price)
                return

            admin_data[user_id]['price'] = price
            message = bot.send_message(user_id, f"Введите url картинки или отправтье картинку в чат:  ", reply_markup=cancel_keyboard())
            bot.register_next_step_handler(message, url_no_subcategory_photo)
            return
        else:
            message = bot.send_message(chat_id=user_id, text=f'Введите цену:', reply_markup=cancel_keyboard())
            bot.register_next_step_handler(message, no_subcategory_price)
    except:
        message = bot.send_message(chat_id=user_id, text=f'Введите цену:', reply_markup=cancel_keyboard())
        bot.register_next_step_handler(message, no_subcategory_price)

def url_no_subcategory_photo(message):
    user_id = message.chat.id
    try:
        global admin_data

        admin_data[user_id]['accounts'] = []
        if message.text is not None:
            url = message.text
            if url.split(':')[0] != 'https':
                message = bot.send_message(user_id, f"Url должен начинаться с https:// ", reply_markup=cancel_keyboard())
                bot.register_next_step_handler(message, url_no_subcategory_photo)
                return
            if requests.get(url).headers['Content-Type'].split('/')[0] != 'image':
                message = bot.send_message(user_id, f"Введите корректный url картинки: ", reply_markup=cancel_keyboard())
                bot.register_next_step_handler(message, url_no_subcategory_photo)
                return
            admin_data[user_id]['img'] = url

        elif message.photo is not None:
            file_info = bot.get_file(message.photo[-1].file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            filepath = 'img/'
            url = filepath + message.photo[0].file_id + '.jpg'
            with open(url, 'wb') as new_file:
                new_file.write(downloaded_file)
            admin_data[user_id]['img'] = url
        else:
            message = bot.send_message(user_id, f"Введите url картинки или отправтье картинку в чат:  ", reply_markup=cancel_keyboard())
            bot.register_next_step_handler(message, url_no_subcategory_photo)

        add_new_no_subcategory(admin_data[user_id])
        admin_data[user_id] = None
        bot.send_message(user_id, 'Успешно')
    except:
        message = bot.send_message(user_id, f"Введите url картинки или отправтье картинку в чат:  ", reply_markup=cancel_keyboard())
        bot.register_next_step_handler(message, url_no_subcategory_photo)