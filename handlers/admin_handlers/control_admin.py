from handlers.handlers import bot
from db import get_user, del_admin_db, add_admin_db
from keyboards import show_all_admin_keyboard, del_yes_no, cancel_keyboard

@bot.message_handler(regexp='^(Добавить администратора)$')
def set_admin(message):
    user_id = message.chat.id
    user = get_user(user_id)
    if user['admin'] == 'superadmin':
    # Добавить логику добавления нового администратора
        message = bot.send_message(user_id, f"Введите username нового пользователя: ", reply_markup=cancel_keyboard())
        bot.register_next_step_handler(message, add_admin)
        pass
    else:
        bot.send_message(user_id, 'Извините, у вас нет прав для этого')


def add_admin(message):
    user_id = message.chat.id
    if message.text is not None:
        username_admin = message.text
        answer = add_admin_db(username_admin)
        if answer is True:
            bot.send_message(user_id, f'{username_admin} успешно стал новым администратором!')
        elif answer is False:
            bot.send_message(user_id, 'Извините, но пользователя с таким никнеймом нет в базе данных, возможно у пользователя которого вы хотите сдлелать администратором скрыт username или он не запускал бота')
            return
    else:
        message = bot.send_message(user_id, f"Введите username нового пользователя: ", reply_markup=cancel_keyboard())
        bot.register_next_step_handler(message, add_admin)


@bot.message_handler(regexp='^(Убрать администратора)$')
def del_admin(message):
    user_id = message.chat.id
    user = get_user(user_id)
    if user['admin'] == 'superadmin':
        bot.send_message(user_id, 'Кого вы хотите убрать?', reply_markup=show_all_admin_keyboard())
    else:
        bot.send_message(user_id, 'Извините, у вас нет прав для этого')


@bot.callback_query_handler(func=lambda call: call.data.split('|')[0] == 'del_admin')
def del_admin(call):
    user_id = call.message.chat.id
    admin_id = call.data.split('|')[1]
    if call.data.split('|')[-1] == 'yes':
        bot.delete_message(user_id, call.message.message_id)
        del_admin_db(int(admin_id))
        bot.send_message(user_id, 'Успешно!')
        return
    elif call.data.split('|')[-1] == 'no':
        bot.delete_message(user_id, call.message.message_id)
        return
    admin_user = get_user(int(admin_id))
    bot.delete_message(user_id, call.message.message_id)
    bot.send_message(user_id, f'Вы уверены что хотите убрать {admin_user["username"]}?', reply_markup=del_yes_no(call.data))
