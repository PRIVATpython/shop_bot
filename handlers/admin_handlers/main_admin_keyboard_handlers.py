from handlers.handlers import bot
from keyboards import add_admin_keyboard, delete_admin_keyboard, change_admin_keyboard, superadmin_keyboard


@bot.message_handler(regexp='^(Добавить)$')
def add_account_category(message):
    user_id = message.chat.id
    bot.send_message(chat_id=user_id, text=f'Выберите из меню ниже: ', reply_markup=add_admin_keyboard())


@bot.message_handler(regexp='^(Удалить)$')
def add_account_category(message):
    user_id = message.chat.id
    bot.send_message(chat_id=user_id, text=f'Выберите из меню ниже: ', reply_markup=delete_admin_keyboard())


@bot.message_handler(regexp='^(Изменить)$')
def add_account_category(message):
    user_id = message.chat.id
    bot.send_message(chat_id=user_id, text=f'Выберите из меню ниже: ', reply_markup=change_admin_keyboard())


@bot.message_handler(regexp='^(Назначить/Убрать администратора)$')
def control_admin_category(message):
    user_id = message.chat.id
    bot.send_message(chat_id=user_id, text='Выберите из меню ниже:', reply_markup=superadmin_keyboard())
