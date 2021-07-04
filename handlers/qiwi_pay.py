from handlers import bot
from handlers import pay_qiwi, pay_test
from db import get_temp_cart
from utilites import check_qiwi_pay

@bot.callback_query_handler(func=lambda call: call.data.split('|')[0] == 'pay_check' and call.data.split('|')[-1] == 'qiwi')
def qiwi_check(call):
    user_id = call.message.chat.id
    temp_cart = get_temp_cart(user_id)
    print(temp_cart)
    answer_qiwi = check_qiwi_pay(comment=temp_cart['comment_pay'], price=temp_cart['all_price'])
    if answer_qiwi is True:
        return pay_test(call)
    return pay_qiwi(call)