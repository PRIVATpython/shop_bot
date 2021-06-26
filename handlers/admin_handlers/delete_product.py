from handlers.handlers import bot
from keyboards import (admin_product_keyboard, admin_no_subcategory_keboard, del_yes_no, admin_category_subcategory_keyboard,
                       admin_service_subcategory_keboard)
from db import get_data_account_no_subcategory, del_no_subcategory_db, get_subcategory, get_subcategory_data, del_subcategory
from db import main_category_subcategory, main_category_no_subcategory


with_cat = main_category_subcategory()
no_cat = main_category_no_subcategory()


@bot.message_handler(regexp='^(Удалить товар)$')
def add_account_category(message):
    global with_cat
    with_cat = main_category_subcategory()
    global no_cat
    no_cat = main_category_no_subcategory()
    user_id = message.chat.id
    category = 'del_goods'
    bot.send_message(chat_id=user_id, text=f'Выберите категорию: ', reply_markup=admin_product_keyboard(category))


@bot.callback_query_handler(func=lambda call: call.data.split('|')[0] == 'del_goods' and call.data.split('|')[1] in no_cat
                                                                                     and call.data.split('|')[2] == 'None')
def del_online_service(call):
    user_id = call.message.chat.id
    category = call.data.split('|')[0]
    bot.delete_message(user_id, call.message.message_id)
    bot.send_message(user_id, f"Выберите какой товар удалить: ", reply_markup=admin_no_subcategory_keboard(category,
                                                                                                           call.data.split('|')[1]))


@bot.callback_query_handler(func=lambda call: call.data.split('|')[0] == 'del_goods' and call.data.split('|')[1] in with_cat
                                                                                     and call.data.split('|')[2] == 'None')
def dell_social(call):
    user_id = call.message.chat.id
    category = call.data.split('|')[0]
    bot.delete_message(user_id, call.message.message_id)
    bot.send_message(user_id, f"Выберите категорию: ", reply_markup=admin_category_subcategory_keyboard(call.data.split('|')[1], category))


@bot.callback_query_handler(func=lambda call: call.data.split('|')[0] == 'del_goods'
                                              and call.data.split('|')[1] in with_cat and call.data.split('|')[3] == 'None')
def dell_goods_social(call):
    user_id = call.message.chat.id
    category = call.data.split('|')[2]
    service = get_subcategory(category)
    bot.delete_message(user_id, call.message.message_id)
    bot.send_message(user_id, f"Выберите товар: ", reply_markup=admin_service_subcategory_keboard(call.data.split('|')[0],
                                                                                                  service['accounts_data']))


@bot.callback_query_handler(func=lambda call: call.data.split('|')[0] == 'del_goods' and call.data.split('|')[1] in no_cat)
def del_online_service(call):
    user_id = call.message.chat.id
    if call.data.split('|')[-1] == 'yes':
        bot.delete_message(user_id, call.message.message_id)
        del_no_subcategory_db(call.data.split('|')[2])
        bot.send_message(chat_id=user_id, text='Удаление успешно выполнено')
        return

    elif call.data.split('|')[-1] == 'no':
        bot.delete_message(user_id, call.message.message_id)
        return

    user_id = call.message.chat.id
    service = call.data.split('|')[2]
    good = get_data_account_no_subcategory(service)
    bot.delete_message(user_id, call.message.message_id)
    bot.send_message(user_id, f"Вы уверены что хотите удалить {good['name']}, список аккаунтов безвровзравтно удалиться ",
                     reply_markup=del_yes_no(call.data))


@bot.callback_query_handler(func=lambda call: call.data.split('|')[0] == 'del_goods' and call.data.split('|')[1] in with_cat)
def dell_goods_social_item(call):
    user_id = call.message.chat.id
    if call.data.split('|')[-1] == 'yes':
        bot.delete_message(user_id, call.message.message_id)
        del_subcategory(call.data.split('|')[2], call.data.split('|')[3])
        bot.send_message(chat_id=user_id, text='Удаление успешно выполнено')
        return

    elif call.data.split('|')[-1] == 'no':
        bot.delete_message(user_id, call.message.message_id)
        return

    service = call.data.split('|')[3]
    good = get_subcategory_data(service)
    bot.delete_message(user_id, call.message.message_id)
    bot.send_message(user_id, f"Вы уверены что хотите удалить {good['name']}, список аккаунтов безвровзравтно удалиться ",
                     reply_markup=del_yes_no(call.data))