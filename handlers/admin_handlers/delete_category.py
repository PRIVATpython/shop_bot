from handlers.handlers import bot
from keyboards import add_category_keyboard, del_yes_no, admin_category_subcategory_keyboard
from db import del_cat_subcategory, get_subcategory


@bot.message_handler(regexp='^(Удалить подкатегорию)$')
def delete_subcategory_main(message):
    user_id = message.chat.id
    category = 'del_cat'
    bot.send_message(chat_id=user_id, text=f'Выберите категорию: ', reply_markup=add_category_keyboard(category))


@bot.callback_query_handler(func=lambda call: call.data.split('|')[0] == 'del_cat' and call.data.split('|')[2] == 'None')
def delete_subcategory_list(call):
    """Only subcategories/delete subcategory - subcategory list"""
    user_id = call.message.chat.id
    category = call.data.split('|')[0]
    bot.delete_message(user_id, call.message.message_id)
    bot.send_message(user_id, f"Выберите категорию: ", reply_markup=admin_category_subcategory_keyboard(call.data.split('|')[1], category))


@bot.callback_query_handler(func=lambda call: call.data.split('|')[0] == 'del_cat' and call.data.split('|')[2] != 'None')
def delete_subcategory(call):
    """Only subcategories/delete subcategory - main page"""
    user_id = call.message.chat.id
    if call.data.split('|')[-1] == 'yes':
        bot.delete_message(user_id, call.message.message_id)
        del_cat_subcategory(call.data.split('|')[2])
        bot.send_message(chat_id=user_id, text='Удаление успешно выполнено')
        return
    elif call.data.split('|')[-1] == 'no':
        bot.delete_message(user_id, call.message.message_id)
        return
    service = call.data.split('|')[2]
    good = get_subcategory(service)
    bot.delete_message(user_id, call.message.message_id)
    bot.send_message(user_id, f"Вы уверены что хотите удалить {good['name']}, список аккаунтов безвровзравтно удалиться ",
                     reply_markup=del_yes_no(call.data))
