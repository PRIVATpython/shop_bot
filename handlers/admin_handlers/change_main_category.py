from handlers.handlers import bot
from db import main_category_subcategory, main_category_no_subcategory
from db import find_no_subcategory_name, find_cat_name, change_main_category_no_sub, change_main_category_sub
from keyboards import admin_product_keyboard, cancel_keyboard


with_cat = main_category_subcategory()
no_cat = main_category_no_subcategory()

admin_data = {}


@bot.message_handler(regexp='^(Изменить главную категорию)$')
def change_main_category_main(message):
    global with_cat
    with_cat = main_category_subcategory()
    global no_cat
    no_cat = main_category_no_subcategory()
    user_id = message.chat.id
    category = 'change_main'
    bot.send_message(user_id, 'Выберите категорию: ', reply_markup=admin_product_keyboard(category))


@bot.callback_query_handler(func=lambda call: call.data.split('|')[0] == 'change_main')
def change_main_category(call):
    global admin_data
    user_id = call.message.chat.id
    bot.delete_message(user_id, call.message.message_id)
    high_id = call.data.split('|')[1]
    admin_data[user_id] = {
        "high_id": high_id
    }
    message = bot.send_message(user_id, f"Введите новое имя категории: ", reply_markup=cancel_keyboard())
    bot.register_next_step_handler(message, set_new_name_main_category)


def set_new_name_main_category(message):
    global admin_data
    user_id = message.chat.id
    if message.text is not None:
        new_name = message.text
        old_name = find_no_subcategory_name(admin_data[user_id]["high_id"])
        if old_name is None:
            old_name = find_cat_name(admin_data[user_id]["high_id"])
            old_name = old_name["name_category"]
            change_main_category_sub(old_name=old_name, new_name=new_name)
            bot.send_message(user_id, f"Успешно!")
            # Добавить логику для изменения SUB main category
        else:
            old_name = old_name["name_category"]
            change_main_category_no_sub(old_name=old_name, new_name=new_name)
            bot.send_message(user_id, f"Успешно!")
    else:
        message = bot.send_message(user_id, f"Введите новое имя категории: ", reply_markup=cancel_keyboard())
        bot.register_next_step_handler(message, set_new_name_main_category)
