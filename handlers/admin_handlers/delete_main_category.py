from handlers.handlers import bot
from keyboards import admin_product_keyboard, del_yes_no
from db import find_no_subcategory_name, find_cat_name, del_main_no_subcategory, del_main_category
from db import main_category_subcategory, main_category_no_subcategory

with_cat = main_category_subcategory()
no_cat = main_category_no_subcategory()


@bot.message_handler(regexp='^(Удалить главную категорию)$')
def delete_main_category_main(message):
    global with_cat
    with_cat = main_category_subcategory()
    global no_cat
    no_cat = main_category_no_subcategory()
    user_id = message.chat.id
    category = 'del_main'
    bot.send_message(user_id, 'Выберите категорию: ', reply_markup=admin_product_keyboard(category))


@bot.callback_query_handler(func=lambda call: call.data.split('|')[0] == 'del_main')
def delete_main_category(call):
    """Both/delete main category - main page"""
    user_id = call.message.chat.id
    category = call.data.split('|')[1]
    bot.delete_message(user_id, call.message.message_id)
    if call.data.split('|')[-1] == 'yes':
        if call.data.split('|')[1] in with_cat:
            del_main_category(call.data.split('|')[1])
            bot.send_message(user_id, 'Успешно')
            return
        elif call.data.split('|')[1] in no_cat:
            del_main_no_subcategory(call.data.split('|')[1])
            bot.send_message(user_id, 'Успешно')
            return
    elif call.data.split('|')[-1] == 'no':
        return

    category_name = find_no_subcategory_name(category)
    if category_name is None:
        category_name = find_cat_name(category)
    bot.send_message(user_id, f'Вы уверены что хотите удалить {category_name["name_category"]}?', reply_markup=del_yes_no(call.data))
