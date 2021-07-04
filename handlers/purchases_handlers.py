from handlers.handlers import bot
from keyboards import purch_product_keyboard
from db import purch_accounts


@bot.message_handler(regexp='^(🛍 Мои покупки)$')
def my_purch(message):
	user_id = message.chat.id
	bot.send_message(message.chat.id, "Выберите товар: ", reply_markup=purch_product_keyboard(user_id))


@bot.callback_query_handler(func=lambda call: call.data.split('|')[0] == 'purch')
def accounts_list_purch(call):
	user_id = call.message.chat.id
	bot.delete_message(user_id, call.message.message_id)
	id = call.data.split('|')[1]
	service = purch_accounts(user_id, id)
	name = service['name']
	accounts = '\n'.join(service['accounts'])
	bot.send_message(chat_id=user_id, text=f'\n{name}\n\n{accounts}')