from handlers.handlers import bot
from keyboards import admin_product_keyboard, admin_category_subcategory_keyboard, cancel_keyboard, clone_img_keyboard
from db import add_new_no_subcategory, add_subcategory
from db import main_category_subcategory, main_category_no_subcategory
from db import find_no_subcategory_name
from db import get_subcategory
import requests


with_cat = main_category_subcategory()
no_cat = main_category_no_subcategory()

admin_data = {}


@bot.message_handler(regexp='^(Добавить новый товар)$')
@bot.callback_query_handler(func=lambda call: call.data.split('|')[0] == 'add_goods' and call.data.split('|')[1] in with_cat and 'back' ==
                                              call.data.split('|')[-1])
def add_account_category(message):
    category = 'add_goods'
    try:
        user_id = message.chat.id
        global with_cat
        with_cat = main_category_subcategory()
        global no_cat
        no_cat = main_category_no_subcategory()
        bot.send_message(chat_id=user_id, text=f'Выберите категорию: ', reply_markup=admin_product_keyboard(category))
    except AttributeError as e:
        bot.delete_message(message.message.chat.id, message.message.message_id)
        bot.send_message(chat_id=message.message.chat.id , text=f'Выберите категорию: ', reply_markup=admin_product_keyboard(category))


@bot.callback_query_handler(func=lambda call: call.data.split('|')[0] == 'add_goods'
                                              and call.data.split('|')[1] in no_cat
                                              and call.data.split('|')[2] == 'None')
def add_product_no_sub(call):
    """No subcategory/add product - main page"""
    global admin_data
    user_id = call.message.chat.id
    category = call.data.split('|')[1]
    name_category = find_no_subcategory_name(category)
    admin_data[user_id] = {
            'name_category': name_category['name_category'],
            'high_id': category
    }
    bot.delete_message(user_id, call.message.message_id)
    message = bot.send_message(user_id, f"Введите название товара: ", reply_markup=cancel_keyboard())
    bot.register_next_step_handler(message, set_product_name_no_sub)


def set_product_name_no_sub(message):
    """No subcategory/add product - name product"""
    global admin_data
    user_id = message.chat.id
    try:
        if message.text is not None:
            name = message.text
            admin_data[user_id]['name'] = name
            message = bot.send_message(user_id, f"Введите цену: ", reply_markup=cancel_keyboard())
            bot.register_next_step_handler(message, set_product_price_no_sub)
            return
        else:
            message = bot.send_message(user_id, f"Введите название для клавиатуры (Только текст): ", reply_markup=cancel_keyboard())
            bot.register_next_step_handler(message, set_product_name_no_sub)
            return
    except:
        message = bot.send_message(user_id, f"Введите название для клавиатуры: ", reply_markup=cancel_keyboard())
        bot.register_next_step_handler(message, set_product_name_no_sub)


def set_product_price_no_sub(message):
    """No subcategory/add product - price product"""
    global admin_data
    user_id = message.chat.id
    try:
        if message.text is not None:
            price = int(message.text)
            if price < 0:
                message = bot.send_message(user_id, f"Цена не может быть отрицательной!:  ", reply_markup=cancel_keyboard())
                bot.register_next_step_handler(message, set_product_price_no_sub)
            admin_data[user_id]['price'] = price
            message = bot.send_message(user_id, f"Введите описание товара:  ", reply_markup=cancel_keyboard())
            bot.register_next_step_handler(message, set_product_description_no_sub)
        else:
            message = bot.send_message(user_id, f"Введите цену (Только цифры): ", reply_markup=cancel_keyboard())
            bot.register_next_step_handler(message, set_product_price_no_sub)
    except:
        message = bot.send_message(user_id, f"Введите цену (Только цифры): ", reply_markup=cancel_keyboard())
        bot.register_next_step_handler(message, set_product_price_no_sub)


def set_product_description_no_sub(message):
    """No subcategory/add product - price product"""
    global admin_data
    user_id = message.chat.id
    try:
        if message.text is not None:
            description = message.text
            admin_data[user_id]['description'] = description
            message = bot.send_message(user_id, f"Введите url картинки:  ", reply_markup=cancel_keyboard())
            bot.register_next_step_handler(message, set_product_img_no_sub)
        else:
            message = bot.send_message(user_id, f"Введите описание (Только текст): ", reply_markup=cancel_keyboard())
            bot.register_next_step_handler(message, set_product_description_no_sub)
    except:
        message = bot.send_message(user_id, f"Введите описание (Только текст): ", reply_markup=cancel_keyboard())
        bot.register_next_step_handler(message, set_product_description_no_sub)


def set_product_img_no_sub(message):
    """No subcategory/add product - image product"""
    global admin_data
    user_id = message.chat.id
    try:
        admin_data[user_id]['accounts'] = []
        if message.text is not None:
            url = message.text
            if url.split(':')[0] != 'https':
                message = bot.send_message(user_id, f"Url должен начинаться с https:// ", reply_markup=cancel_keyboard())
                bot.register_next_step_handler(message, set_product_img_no_sub)
                return
            if requests.get(url).headers['Content-Type'].split('/')[0] != 'image':
                message = bot.send_message(user_id, f"Введите корректный url картинки: ", reply_markup=cancel_keyboard())
                bot.register_next_step_handler(message, set_product_img_no_sub)
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
            message = bot.send_message(user_id, f"Введите url картинки или пришлите картинку в чат (Либо ссылка"
                                                f" изображения начинающаяся с https:// или фото ):  ",
                                       reply_markup=cancel_keyboard())
            bot.register_next_step_handler(message, set_product_img_no_sub)

        add_new_no_subcategory(admin_data[user_id])
        admin_data[user_id] = None
        bot.send_message(user_id, 'Успешно')
    except:
        message = bot.send_message(user_id,
                                   f"Введите url картинки или пришлите картинку в чат (Либо ссылка изображения"
                                   f" начинающаяся с https:// или фото ):  ",
                                   reply_markup=cancel_keyboard())
        bot.register_next_step_handler(message, set_product_img_no_sub)

############################################################################################################################################


@bot.callback_query_handler(func=lambda call: call.data.split('|')[0] == 'add_goods' and call.data.split('|')[1] in with_cat
                                              and call.data.split('|')[2] == 'None')
def add_product_sub_list(call):
    """Subcategory/add product - subcategory list"""
    user_id = call.message.chat.id
    category = 'add_goods'
    bot.delete_message(user_id, call.message.message_id)
    keyboard = admin_category_subcategory_keyboard(call.data.split('|')[1], category)
    bot.send_message(chat_id=user_id, text=f'Выберите категорию: ', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data.split('|')[0] == 'add_goods' and call.data.split('|')[1] in with_cat
                                              and call.data.split('|')[2] != 'None')
def add_product_sub(call):
    """Subcategory/add product - main page"""
    global admin_data
    user_id = call.message.chat.id
    high_id = call.data.split('|')[2]
    admin_data[user_id] = {

            'category': call.data.split('|')[1],
            'high_id': high_id

    }
    bot.delete_message(user_id, call.message.message_id)
    message = bot.send_message(user_id, f"Введите название товара: ", reply_markup=cancel_keyboard())
    bot.register_next_step_handler(message, set_product_name_sub)


def set_product_name_sub(message):
    """Subcategory/add product - name product"""
    global admin_data
    user_id = message.chat.id
    try:
        if message.text is not None:
            name = message.text
            admin_data[user_id]['name'] = name
            message = bot.send_message(user_id, f"Введите цену: ", reply_markup=cancel_keyboard())
            bot.register_next_step_handler(message, set_product_price_sub)
        else:
            message = bot.send_message(user_id, f"Введите название товара (Только текст): ", reply_markup=cancel_keyboard())
            bot.register_next_step_handler(message, set_product_name_sub)
    except:
        message = bot.send_message(user_id, f"Введите название товара (Только текст): ", reply_markup=cancel_keyboard())
        bot.register_next_step_handler(message, set_product_name_sub)


def set_product_price_sub(message):
    """Subcategory/add product - price product"""
    global admin_data
    user_id = message.chat.id
    try:
        if message.text is not None:
            price = int(message.text)
            if price < 0:
                message = bot.send_message(user_id, f"Цена не может быть отрицательной!", reply_markup=cancel_keyboard())
                bot.register_next_step_handler(message, set_product_price_sub)

            admin_data[user_id]['price'] = price
            message = bot.send_message(user_id, f"Введите описание: ", reply_markup=cancel_keyboard())
            bot.register_next_step_handler(message, set_product_description_sub)
        else:
            message = bot.send_message(user_id, f"Введите цену (Только цифры): ", reply_markup=cancel_keyboard())
            bot.register_next_step_handler(message, set_product_price_sub)
    except:
        message = bot.send_message(user_id, f"Введите цену (Только цифры): ", reply_markup=cancel_keyboard())
        bot.register_next_step_handler(message, set_product_price_sub)


def set_product_description_sub(message):
    """Subcategory/add product - description product"""
    global admin_data
    user_id = message.chat.id
    try:

        if message.text is not None:
            description = message.text
            admin_data[user_id]['description'] = description
            message = bot.send_message(user_id, f"Введите url картинки или пришлите картинку в чат: ", reply_markup=clone_img_keyboard())
            bot.register_next_step_handler(message, set_product_image_sub)
        else:
            message = bot.send_message(user_id, f"Введите описание (Только текст): ", reply_markup=cancel_keyboard())
            bot.register_next_step_handler(message, set_product_description_sub)
    except:
        message = bot.send_message(user_id, f"Введите описание (Только текст): ", reply_markup=cancel_keyboard())
        bot.register_next_step_handler(message, set_product_description_sub)


@bot.callback_query_handler(func=lambda call: call.data.split('|')[0] == 'get_subcat_img')
def get_subcat_img(call):
    """Subcategory/add product - get main category image"""
    global admin_data
    user_id = call.message.chat.id
    bot.clear_step_handler_by_chat_id(chat_id=user_id)
    bot.delete_message(user_id, call.message.message_id)
    service = get_subcategory(admin_data[user_id]['high_id'])
    admin_data[user_id]['img'] = service['img']
    add_subcategory(admin_data[user_id])
    admin_data[user_id] = None
    bot.send_message(user_id, 'Успешно')


def set_product_image_sub(message):
    """Subcategory/add product - image product"""
    global admin_data
    user_id = message.chat.id
    try:
        if message.text is not None:
            img = message.text
            if img.split(':')[0] != 'https':
                message = bot.send_message(user_id, f"Url должен начинаться с https:// ", reply_markup=clone_img_keyboard())
                bot.register_next_step_handler(message, set_product_image_sub)
                return
            if requests.get(img).headers['Content-Type'].split('/')[0] != 'image':
                message = bot.send_message(user_id, f"Введите корректный url картинки: ", reply_markup=clone_img_keyboard())
                bot.register_next_step_handler(message, set_product_image_sub)
                return
            admin_data[user_id]['img'] = img
        elif message.photo is not None:
            file_info = bot.get_file(message.photo[-1].file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            filepath = 'img/'
            url = filepath + message.photo[0].file_id + '.jpg'
            with open(url, 'wb') as new_file:
                new_file.write(downloaded_file)
            admin_data[user_id]['img'] = url
        else:
            message = bot.send_message(user_id, f"Введите url картинки или пришлите картинку в чат: ", reply_markup=clone_img_keyboard())
            bot.register_next_step_handler(message, set_product_image_sub)
            return
        add_subcategory(admin_data[user_id])
        admin_data[user_id] = None
        bot.send_message(user_id, 'Успешно')
    except:
        message = bot.send_message(user_id, f"Введите url картинки или пришлите картинку в чат: ", reply_markup=clone_img_keyboard())
        bot.register_next_step_handler(message, set_product_image_sub)
