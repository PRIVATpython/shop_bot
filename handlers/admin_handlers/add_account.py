from handlers.handlers import bot
from keyboards import (admin_product_keyboard, cancel_keyboard, admin_no_subcategory_keboard,
                       admin_category_subcategory_keyboard, admin_service_subcategory_keyboard)
from db import set_temp_data_admin, get_user
from db import get_subcategory, add_subcategory_account, main_category_subcategory
from db import main_category_no_subcategory, add_no_subcategory_account
from keyboards import generation_account_keyboard
from utilites import generate_cd_key, generator_normal_acc

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
    """Cancel input admin"""
    user_id = call.message.chat.id
    bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
    bot.delete_message(user_id, call.message.message_id)


############################################################################################################################################


@bot.callback_query_handler(func=lambda call: call.data.split('|')[0] == 'add_acc'
                                              and call.data.split('|')[1] in no_cat
                                              and call.data.split('|')[2] == 'None')
def add_account_no_subcategory(call):
    """No subcategory/add account - product list"""
    user_id = call.message.chat.id
    category = call.data.split('|')[0]
    bot.delete_message(user_id, call.message.message_id)
    keyboard = admin_no_subcategory_keboard(category, call.data.split('|')[1])
    bot.send_message(chat_id=user_id, text=f'Выберите куда добавить аккаунты: ', reply_markup=keyboard)


@bot.callback_query_handler(
    func=lambda call: call.data.split('|')[0] == 'add_acc' and call.data.split('|')[1] in no_cat and call.data.split('|')[2] not in [
        'normal_acc', 'cd_key'])
def add_account(call):
    """No subcategory/add account - input accounts"""
    user_id = call.message.chat.id
    set_temp_data_admin(user_id, call.data)
    bot.delete_message(user_id, call.message.message_id)
    message = bot.send_message(user_id,
                               f"\n\nЕсли вы передумали, напишите 'выйти'\n"
                               f"Введите аккаунты в формате login|password\n"
                               f"Для добавления нескольких аккаунтов вводите их с новой строки",
                               reply_markup=generation_account_keyboard(call.data.split('|')[1]))
    bot.register_next_step_handler(message, input_accounts)


@bot.callback_query_handler(func=lambda call: call.data.split('|')[0] == 'add_acc' and call.data.split('|')[-1] in ['normal_acc', 'cd_key'])
def generator_accounts(call):
    """Both/add account - main generator accounts"""
    user_id = call.message.chat.id
    bot.clear_step_handler_by_chat_id(chat_id=user_id)
    bot.delete_message(user_id, call.message.message_id)
    if call.data.split('|')[2] == 'normal_acc':
        message = bot.send_message(user_id,
                                   f"Сколько аккаунтов добавить? (Введите цифру)")
        bot.register_next_step_handler(message, generator_normal_account)
        return
    elif call.data.split('|')[2] == 'cd_key':
        message = bot.send_message(user_id,
                                   f"Сколько ключей добавить? (Введите цифру)")
        bot.register_next_step_handler(message, generator_cd_key)
        return

############################################################################################################################################

@bot.callback_query_handler(
    func=lambda call: call.data.split('|')[0] == 'add_acc' and call.data.split('|')[1] in with_cat and call.data.split('|')[2] == 'None')
@bot.callback_query_handler(
    func=lambda call: call.data.split('|')[0] == 'add_acc' and call.data.split('|')[1] in with_cat and call.data.split('|')[-1] == 'back')
def add_account_subcategory(call):
    """Subcategory/add account - subcategory list"""
    user_id = call.message.chat.id
    category = 'add_acc'
    bot.delete_message(user_id, call.message.message_id)
    keyboard = admin_category_subcategory_keyboard(call.data.split('|')[1], category)
    bot.send_message(chat_id=user_id, text=f'Выберите категорию: ', reply_markup=keyboard)


@bot.callback_query_handler(
    func=lambda call: call.data.split('|')[0] == 'add_acc' and call.data.split('|')[1] in with_cat and call.data.split('|')[-1] == 'None')
def add_account(call):
    """Subcategory/add account - product list"""
    user_id = call.message.chat.id
    category = call.data.split('|')[2]
    service = get_subcategory(category)
    keyboard = admin_service_subcategory_keyboard(call.data.split('|')[0], service['accounts_data'])
    bot.delete_message(user_id, call.message.message_id)
    bot.send_message(chat_id=user_id, text=f'Выберите аккаунт: ', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data.split('|')[0] == 'add_acc' and call.data.split('|')[1] in with_cat)
def add_account(call):
    """Subcategory/add account - input accounts"""
    user_id = call.message.chat.id
    set_temp_data_admin(user_id, call.data)
    bot.delete_message(user_id, call.message.message_id)
    message = bot.send_message(user_id,
                               f"\nЕсли вы передумали, напишите 'выйти'\n"
                               f"Введите аккаунты в формате login|password\n"
                               f"Для добавления нескольких аккаунтов вводите их с новой строки",
                               reply_markup=generation_account_keyboard(call.data.split('|')[1]))
    bot.register_next_step_handler(message, input_accounts)

############################################################################################################################################

def input_accounts(message):
    """Both/add account - Handinput add accounts"""
    user_id = message.chat.id
    if message.text is None:
        message = bot.send_message(user_id,
                                   f"\nЕсли вы передумали, напишите 'выйти'\n"
                                   f"Введите аккаунты в формате login|password\n"
                                   f"Для добавления нескольких аккаунтов вводите их с новой строки",
                                   reply_markup=cancel_keyboard())
        bot.register_next_step_handler(message, input_accounts)
        return
    account = message.text.split('\n')
    callback = get_user(message.chat.id)
    callback = callback['temp_data_admin']
    if account[0] == 'выйти':
        bot.send_message(message.chat.id, 'Выход')
        return
    for item in account:
        if callback.split('|')[1] in no_cat:
            add_no_subcategory_account(callback.split('|')[2], item)
        elif callback.split('|')[1] in with_cat:
            add_subcategory_account(callback.split('|')[3], item)
    set_temp_data_admin(user_id, ' ')
    bot.send_message(message.chat.id, 'Аккаунты добавлены в базу данных')


def generator_normal_account(message):
    """Generator accounts type - email@mail.com|password"""
    user_id = message.chat.id
    try:
        if message.text is not None:
            count = int(message.text)
            if count <= 0:
                message = bot.send_message(user_id,
                                           f"Количество не может быть равно 0 или быть отрицательным")
                bot.register_next_step_handler(message, generator_normal_account)
                return
            elif count > 150:
                message = bot.send_message(user_id,
                                           f"Не больше 150 аккаунтов за раз")
                bot.register_next_step_handler(message, generator_normal_account)
                return
            login_list = generator_normal_acc(count)
            callback = get_user(message.chat.id)
            callback = callback['temp_data_admin']
            for item in login_list:
                print(item)
                if callback.split('|')[1] in no_cat:
                    add_no_subcategory_account(callback.split('|')[2], item)
                elif callback.split('|')[1] in with_cat:  # в соицал не добавляет аккаунты
                    add_subcategory_account(callback.split('|')[3], item)
            bot.send_message(chat_id=user_id, text=f'Успешно!')
        else:
            message = bot.send_message(user_id,
                                       f"Сколько аккаунтов добавить? (Введите цифру)")
            bot.register_next_step_handler(message, generator_normal_account)
            return
    except:
        message = bot.send_message(user_id,
                                   f"Сколько аккаунтов добавить? (Введите цифру)")
        bot.register_next_step_handler(message, generator_normal_account)


def generator_cd_key(message):
    """Generator accounts type - xxxxx-xxxxx-xxxxx-xxxxx"""
    user_id = message.chat.id
    try:
        if message.text is not None:
            count = int(message.text)
            if count <= 0:
                message = bot.send_message(user_id,
                                           f"Количество не может быть равно 0 или быть отрицательным")
                bot.register_next_step_handler(message, generator_cd_key)
                return
            elif count > 150:
                message = bot.send_message(user_id,
                                           f"Не больше 150 аккаунтов за раз")
                bot.register_next_step_handler(message, generator_cd_key)
                return
            key_list = generate_cd_key(count)
            callback = get_user(message.chat.id)
            callback = callback['temp_data_admin']
            for item in key_list:
                print(item)
                if callback.split('|')[1] in no_cat:
                    add_no_subcategory_account(callback.split('|')[2], item)
                elif callback.split('|')[1] in with_cat:  # в соицал не добавляет аккаунты
                    add_subcategory_account(callback.split('|')[3], item)
            bot.send_message(chat_id=user_id, text=f'Успешно!')
        else:
            message = bot.send_message(user_id,
                                       f"Сколько ключей добавить? (Введите цифру)")
            bot.register_next_step_handler(message, generator_cd_key)
            return
    except:
        message = bot.send_message(user_id,
                                   f"Сколько ключей добавить? (Введите цифру)")
        bot.register_next_step_handler(message, generator_cd_key)
