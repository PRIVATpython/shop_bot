from handlers.handlers import bot
from keyboards import add_category_keyboard, cancel_keyboard
from db import add_new_cat_subcategory, find_cat_name
import requests

admin_data = {}


@bot.message_handler(regexp='^(Добавить новую подкатегорию)$')
def add_account_category(message):
    user_id = message.chat.id
    category = 'add_cat'
    # bot.delete_message(user_id, call.message.message_id)
    bot.send_message(chat_id=user_id, text=f'Куда добавить категорию?', reply_markup=add_category_keyboard(category))


@bot.callback_query_handler(func=lambda call: call.data.split('|')[0] == 'add_cat')
def add_category(call):
    user_id = call.message.chat.id
    service = find_cat_name(call.data.split('|')[1])
    global admin_data
    admin_data[user_id] = {

            'name_category': service['name_category'],
            'high_id': call.data.split('|')[1]

    }
    bot.delete_message(user_id, call.message.message_id)
    message = bot.send_message(user_id, f"Введите название категории: ", reply_markup=cancel_keyboard())
    bot.register_next_step_handler(message, set_name_category)


def set_name_category(message):
    global admin_data
    user_id = message.chat.id
    try:
        if message.text is None:
            message = bot.send_message(user_id, f"Введите название категории: ", reply_markup=cancel_keyboard())
            bot.register_next_step_handler(message, set_name_category)
            return
        name = message.text
        admin_data[user_id]['name'] = name
        message = bot.send_message(user_id, f"Введите url картинки: ", reply_markup=cancel_keyboard())
        bot.register_next_step_handler(message, set_url_img_cat)
    except:
        message = bot.send_message(user_id, f"Введите название категории: ", reply_markup=cancel_keyboard())
        bot.register_next_step_handler(message, set_name_category)

def set_url_img_cat(message):
    global admin_data
    user_id = message.chat.id
    try:
        if message.text is not None:
            url = message.text
            if url.split(':')[0] != 'https':
                message = bot.send_message(user_id, f"Url должен начинаться с https:// ", reply_markup=cancel_keyboard())
                bot.register_next_step_handler(message, set_url_img_cat)
                return
            if requests.get(url).headers['Content-Type'].split('/')[0] != 'image':
                message = bot.send_message(user_id, f"Введите корректный url картинки: ", reply_markup=cancel_keyboard())
                bot.register_next_step_handler(message, set_url_img_cat)
                return

        elif message.photo is not None:
            file_info = bot.get_file(message.photo[-1].file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            filepath = 'img/'
            url = filepath + message.photo[0].file_id + '.jpg'
            with open(url, 'wb') as new_file:
                new_file.write(downloaded_file)
            # url = open(url , 'rb')

        else:
            message = bot.send_message(user_id, f"Введите url картинки или пришлите картинку в чат: ", reply_markup=cancel_keyboard())
            bot.register_next_step_handler(message, set_url_img_cat)
            return

        admin_data[user_id]['img'] = url
        add_new_cat_subcategory(admin_data[user_id])
        admin_data[user_id] = None
        bot.send_message(user_id, 'Успешно добавлено')
    except:
        message = bot.send_message(user_id, f"Введите url картинки или пришлите картинку в чат: ", reply_markup=cancel_keyboard())
        bot.register_next_step_handler(message, set_url_img_cat)