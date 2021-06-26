# from handlers.handlers import bot
# from db import set_default_temp_cart, get_subcategory_data, get_subcategory, set_count_temp_cart, get_or_create_user, set_temp_cart
# from db import main_category_subcategory
# from keyboards import category_subcategory_keyboard, subcategory_keyboard, buy_keyboard
# from db import main_category_subcategory
#
#
#
#
#
# @bot.callback_query_handler(func=lambda call: call.data.split('|')[0] in with_cat and call.data.split('|')[3] == 'buy')
# def subcategory_buy(call):  # Управление кол-вом
#     user_id = call.message.chat.id
#     social_network_data = get_subcategory_data(call.data.split('|')[2])  # исправить
#     set_temp_cart(user_id, social_network_data, call.data.split('|')[0])
#     answer = set_count_temp_cart(user_id, social_network_data, int(call.data.split('|')[4]), call.data.split('|')[0])
#     if answer is False:
#         bot.answer_callback_query(call.id, text='Минимальное количество товара: 1 шт')
#     elif answer is True:
#         user = get_or_create_user(call.message.chat)
#         bot.answer_callback_query(call.id, text=f'Максимальное количество товара: {user["temp_cart"]["count"]} шт.')
#     return subcategory_data_prod(call)
#
#
# @bot.callback_query_handler(func=lambda call: call.data.split('|')[0] in with_cat and call.data.split('|')[1] != 'main' and
#                                               call.data.split('|')[2] != 'None' and call.data.split('|')[2] != 'back')
# def subcategory_data_prod(call):  # Страница товара
#     user_id = call.message.chat.id
#     social_network_data = get_subcategory_data(call.data.split('|')[2])
#     set_temp_cart(user_id, social_network_data, call.data.split('|')[0])
#     text = social_network_text(social_network_data)
#     user = get_or_create_user(call.message.chat)
#     bot.delete_message(user_id, call.message.message_id)
#
#     photo = social_network_data['img']
#     if photo.split('/')[0] == 'img':
#         photo = open(photo, 'rb')
#
#     bot.send_photo(chat_id=user_id, photo=photo, caption=text,
#                    reply_markup=buy_keyboard(count=user['temp_cart']['count'],
#                                              service=f"{call.data.split('|')[0]}|{call.data.split('|')[1]}|{call.data.split('|')[2]}",
#                                              back=f"{call.data.split('|')[0]}|{call.data.split('|')[1]}"))
#
#
# @bot.callback_query_handler(func=lambda call: call.data.split('|')[0] in with_cat and call.data.split('|')[1] != 'main')
# @bot.callback_query_handler(func=lambda call: call.data.split('|')[0] in with_cat and call.data.split('|')[3] == 'back')
# def social_network_instagram(call):
#     user_id = call.message.chat.id
#     category = get_subcategory(call.data.split('|')[1])
#     bot.answer_callback_query(call.id)
#     bot.delete_message(user_id, call.message.message_id)
#
#     photo = category['img']
#     if photo.split('/')[0] == 'img':
#         photo = open(photo, 'rb')
#
#     bot.send_photo(chat_id=user_id, photo=photo, caption='Выберите аккаунт:',
#                    reply_markup=subcategory_keyboard(call.data.split('|')[0], call.data.split('|')[1]))
#
#
# def social_network_text(service):
#     text = f"""{service['name'].upper()} 🎥
#
# Цена: {service['price']} рублей
#
# Доступно: {len(service['accounts'])} шт
#
# ➖➖➖➖➖➖➖➖➖➖➖➖
# 📃 Категория:PREMIUM
# 💰 Цена: ‼️{service['price']} ₽
# 📃 Описание: {service['description']}
# ➖➖➖➖➖➖➖➖➖➖➖➖"""
#     return text
