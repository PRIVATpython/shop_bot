from handlers.handlers import bot
from keyboards import (admin_product_keyboard, cancel_keyboard, admin_no_subcategory_keboard,
                       admin_category_subcategory_keyboard, admin_service_subcategory_keboard)
from db import set_temp_data_admin, get_user
from db import get_subcategory, add_subcategory_account, main_category_subcategory
from db import main_category_no_subcategory, add_no_subcategory_account

with_cat = main_category_subcategory()
no_cat = main_category_no_subcategory()


@bot.message_handler(regexp='^(Добавить аккаунты)$')
def add_account_category(message):
    global with_cat
    with_cat = main_category_subcategory()
    global no_cat
    no_cat = main_category_no_subcategory()
    user_id = message.chat.id
    category = 'add_acc'
    bot.send_message(chat_id=user_id, text=f'Выберите категорию: ', reply_markup=admin_product_keyboard(category))


@bot.callback_query_handler(func=lambda call: call.data.split('|')[0] == 'cancel_input')
def cancel_input(call):
    user_id = call.message.chat.id
    bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
    bot.delete_message(user_id, call.message.message_id)

####NO_SUBCATEGORY
@bot.callback_query_handler(func=lambda call: call.data.split('|')[0] == 'add_acc'
                                              and call.data.split('|')[1] in no_cat
                                              and call.data.split('|')[2] == 'None')
def add_account_online_subcategory(call):
    user_id = call.message.chat.id
    category = call.data.split('|')[0]
    bot.delete_message(user_id, call.message.message_id)
    keyboard = admin_no_subcategory_keboard(category, call.data.split('|')[1])
    bot.send_message(chat_id=user_id, text=f'Выберите куда добавить аккаунты: ', reply_markup=keyboard)

####SUBCATEGORY
@bot.callback_query_handler(
    func=lambda call: call.data.split('|')[0] == 'add_acc' and call.data.split('|')[1] in with_cat and call.data.split('|')[2] == 'None')
@bot.callback_query_handler(
    func=lambda call: call.data.split('|')[0] == 'add_acc' and call.data.split('|')[1] in with_cat and call.data.split('|')[-1] == 'back')
def add_social_subcategory(call):
    user_id = call.message.chat.id
    category = 'add_acc'
    bot.delete_message(user_id, call.message.message_id)
    keyboard = admin_category_subcategory_keyboard(call.data.split('|')[1], category)
    bot.send_message(chat_id=user_id, text=f'Выберите категорию: ', reply_markup=keyboard)

####NO_SUBCATEGORY
@bot.callback_query_handler(func=lambda call: call.data.split('|')[0] == 'add_acc' and call.data.split('|')[1] in no_cat)
def add_account(call):
    user_id = call.message.chat.id
    set_temp_data_admin(user_id, call.data)
    bot.delete_message(user_id, call.message.message_id)
    message = bot.send_message(user_id,
                               f"\n\nЕсли вы передумали, напишите 'выйти'\n"
                               f"Введите аккаунты в формате login|password\n"
                               f"Для добавления нескольких аккаунтов вводите их с новой строки",
                               reply_markup=cancel_keyboard())
    bot.register_next_step_handler(message, reply_to_user)


####SUBCATEGORY
@bot.callback_query_handler(
    func=lambda call: call.data.split('|')[0] == 'add_acc' and call.data.split('|')[1] in with_cat and call.data.split('|')[-1] == 'None')
def add_account(call):
    user_id = call.message.chat.id
    category = call.data.split('|')[2]
    service = get_subcategory(category)
    keyboard = admin_service_subcategory_keboard(call.data.split('|')[0], service['accounts_data'])
    bot.delete_message(user_id, call.message.message_id)
    bot.send_message(chat_id=user_id, text=f'Выберите аккаунт: ', reply_markup=keyboard)


####SUBCATEGORY
@bot.callback_query_handler(func=lambda call: call.data.split('|')[0] == 'add_acc' and call.data.split('|')[1] in with_cat)
def add_account(call):
    user_id = call.message.chat.id
    set_temp_data_admin(user_id, call.data)
    bot.delete_message(user_id, call.message.message_id)
    message = bot.send_message(user_id,
                               f"\nЕсли вы передумали, напишите 'выйти'\n"
                               f"Введите аккаунты в формате login|password\n"
                               f"Для добавления нескольких аккаунтов вводите их с новой строки",
                               reply_markup=cancel_keyboard())
    bot.register_next_step_handler(message, reply_to_user)




def reply_to_user(message):
    user_id = message.chat.id
    if message.text is None:
        message = bot.send_message(user_id,
                                   f"\nЕсли вы передумали, напишите 'выйти'\n"
                                   f"Введите аккаунты в формате login|password\n"
                                   f"Для добавления нескольких аккаунтов вводите их с новой строки",
                                   reply_markup=cancel_keyboard())
        bot.register_next_step_handler(message, reply_to_user)
        return
    account = message.text.split('\n')
    callback = get_user(message.chat.id)
    callback = callback['temp_data_admin']
    if account[0] == 'выйти':
        bot.send_message(message.chat.id, 'Выход')
        return None
    for item in account:
        if callback.split('|')[1] in no_cat:
            add_no_subcategory_account(callback.split('|')[2], item)
        elif callback.split('|')[1] in with_cat:  # в соицал не добавляет аккаунты
            add_subcategory_account(callback.split('|')[3], item)
    set_temp_data_admin(user_id, ' ')
    bot.send_message(message.chat.id, 'Аккаунты добавлены в базу данных')
