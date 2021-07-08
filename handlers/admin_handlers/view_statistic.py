from handlers import bot
from db import main_category_subcategory, main_category_no_subcategory, show_statistic_no_sub, get_data_account_no_subcategory
from keyboards import admin_product_keyboard, admin_no_subcategory_keboard, period_statistic_no_sub

with_cat = main_category_subcategory()
no_cat = main_category_no_subcategory()


@bot.message_handler(regexp='^(Посмотреть статистику)$')
def view_statistic(message):
    global with_cat
    with_cat = main_category_subcategory()
    global no_cat
    no_cat = main_category_no_subcategory()
    user_id = message.chat.id
    category = 'view_statistic'
    bot.send_message(chat_id=user_id, text=f'Выберите категорию: ', reply_markup=admin_product_keyboard(category))


@bot.callback_query_handler(func=lambda call: call.data.split('|')[0] == 'view_statistic'
                                              and call.data.split('|')[1] in no_cat
                                              and call.data.split('|')[2] == 'None')
def view_statistic_no_sub(call):
    user_id = call.message.chat.id
    category = call.data.split('|')[0]
    bot.delete_message(user_id, call.message.message_id)
    keyboard = admin_no_subcategory_keboard(category, call.data.split('|')[1])
    bot.send_message(chat_id=user_id, text=f'Выберите товар: ', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data.split('|')[0] == 'view_statistic'
                                              and call.data.split('|')[1] in no_cat)
def view_statistic_period(call):
    user_id = call.message.chat.id
    try:
        period = int(call.data.split("|")[-1])
        count, sum = show_statistic_no_sub(period=period, service_id=call.data.split('|')[2])
        service = get_data_account_no_subcategory(call.data.split("|")[2])
        price = service['price']
        bot.delete_message(user_id, call.message.message_id)
        bot.send_message(user_id, f"За этот период было проданно {count} аккаунтов на сумму {sum} рублей")
    except Exception as e:
        callback_for_keyboards = call.data.split('|', 1)[1]
        keyboard = period_statistic_no_sub(callback_for_keyboards)
        bot.delete_message(user_id, call.message.message_id)
        bot.send_message(user_id, "Выберите период", reply_markup=keyboard)

# СТАТИСТИКА ДЛЯ SUB КАТЕГОРИИ

