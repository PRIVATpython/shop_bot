# from handlers.handlers import bot
# from keyboards import account_no_subcategory_keyboard, buy_keyboard
# from db import get_or_create_user, set_temp_cart, set_count_temp_cart, set_default_temp_cart
# from db import main_category_no_subcategory, get_data_account_no_subcategory
#
# no_cat = main_category_no_subcategory()
#
#
# @bot.callback_query_handler(func=lambda call: call.data.split('|')[0] in no_cat and call.data.split('|')[1] == 'main')
# @bot.callback_query_handler(func=lambda call: call.data.split('|')[0] in no_cat and call.data.split('|')[1] == 'back')
# def main_no_subcategory(call):
#     global no_cat
#     no_cat = main_category_no_subcategory()
#     user_id = call.message.chat.id
#     bot.answer_callback_query(call.id)
#     bot.delete_message(user_id, call.message.message_id)
#     set_default_temp_cart(user_id)
#     bot.send_message(user_id, text='Выберите товар: ', reply_markup=account_no_subcategory_keyboard(call.data.split('|')[0]))
#
#
# @bot.callback_query_handler(func=lambda call: call.data.split('|')[0] in no_cat and call.data.split('|')[1] != 'main')
# def account_no_subcategory(call):
#     user_id = call.message.chat.id
#     callback = call.data.split('|')[1]
#     service = get_data_account_no_subcategory(callback)
#     if call.data.split('|')[2] == 'buy':
#         count = int(call.data.split('|')[3])
#         answer = set_count_temp_cart(user_id, service, count, call.data.split('|')[0])
#         if answer is False:
#             bot.answer_callback_query(call.id, text='Минимальное количество товара: 1 шт.')
#         elif answer is True:
#             user = get_or_create_user(call.message.chat)
#             bot.answer_callback_query(call.id, text=f'Макисмальное количество товара: {user["temp_cart"]["count"]} шт.')
#     bot.delete_message(user_id, call.message.message_id)
#     user = get_or_create_user(call.message.chat)
#     set_temp_cart(user['user_id'], service, call.data.split('|')[0])    # задает имя сервиса во временной коризне
#     text = account_no_subcategory_text(service)
#     photo = service['img']
#     if photo.split('/')[0] == 'img':
#         photo = open(photo, 'rb')
#     bot.send_photo(chat_id=call.message.chat.id, photo=photo, caption=text,
#                    reply_markup=buy_keyboard(count=user['temp_cart']['count'],
#                                              service=f"{call.data.split('|')[0]}|{call.data.split('|')[1]}",
#                                              back=call.data.split('|')[0]))
#
#
# def account_no_subcategory_text(service):
#     text = f"""{service['name'].upper()} PREMIUM - ПОДПИСКА НАВСЕГДА 🎥
#
# Цена: {service['price']} рублей
#
# Доступно: {len(service['accounts'])} шт
#
# ➖➖➖➖➖➖➖➖➖➖➖➖
# 📃 Категория:PREMIUM
# 💰 Цена: ‼️300/{service['price']} ₽
# 📃 Описание: Гарантия после покупки 60 минут
# Выберите количество товара, которое хотите купить:
# ➖➖➖➖➖➖➖➖➖➖➖➖"""
#     return text
