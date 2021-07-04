from handlers.handlers import bot
from db import get_or_create_user
from keyboards import main_keyboard, main_admin_keyboard


@bot.message_handler(commands=['start', 'help'])
@bot.message_handler(regexp='^(Назад к главному меню)$')
def command_start(message):
	get_or_create_user(message.from_user)
	bot.send_message(message.chat.id, "Добро пожаловать в наш магазин", reply_markup=main_keyboard())


@bot.message_handler(commands=['admin', 'superadmin'])
@bot.message_handler(regexp='^(Назад)$')
def command_start(message):
	user = get_or_create_user(message.from_user)
	if user['admin'] == 'admin':
		bot.send_message(message.chat.id, "Я хочу что-то: ", reply_markup=main_admin_keyboard())



