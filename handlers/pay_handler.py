# from handlers.handlers import bot
# from db import get_temp_cart, give_account_no_subcategory, give_account_subcategory
# from keyboards import pay_keyboard
# from db import main_category_subcategory, main_category_no_subcategory
#
# with_cat = main_category_subcategory()
# no_cat = main_category_no_subcategory()
#
#
# @bot.callback_query_handler(func=lambda call: call.data.split('|')[0] == 'pay' and call.data.split('|')[-1] == 'test')
# def pay_test(call):
#     user_id = call.message.chat.id
#     category = call.data.split('|')[1]
#     if category in no_cat:
#         accounts = give_account_no_subcategory(user_id)
#     elif category in with_cat:
#         accounts = give_account_subcategory(user_id)
#     accounts = '\n'.join(accounts)
#     bot.delete_message(user_id, call.message.message_id)
#     bot.send_message(chat_id=user_id, text=f'Спасибо за покупку!\n\n{accounts}')
#
#
# @bot.callback_query_handler(func=lambda call: call.data.split('|')[0] == 'pay')
# def pay_handler(call):
#     user_id = call.message.chat.id
#     temp_cart = get_temp_cart(user_id)
#     bot.delete_message(user_id, call.message.message_id)
#     bot.send_message(chat_id=user_id, text=f'Товар: {temp_cart["product"]}\n\nЦена: {temp_cart["price"]}\n\n'
#                                            f'Кол-во: {temp_cart["count"]}\n\nЦена за все: {temp_cart["count"] * temp_cart["price"]}',
#                      reply_markup=pay_keyboard(call.data.split('|')[1]),
#                      parse_mode='HTML')
#
