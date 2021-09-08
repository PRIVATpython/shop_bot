from handlers import bot
from keyboards import main_games_keyboard, game_yes_no, encode_roulette_keyboard, decode_roulette_keyboard, cancel_keyboard, lvl_keyboard
from db import get_user, set_rate_db, set_prize_bonus

temp_data = {}


@bot.message_handler(regexp='^(⚙ Мои баллы)$')
def games_main(message):
    bot.send_message(chat_id=message.chat.id, text='Во что хотите сыграть?', reply_markup=main_games_keyboard())


@bot.message_handler(regexp='^(Мои бонусы)$')
def games_main(message):
    user_data = get_user(message.chat.id)
    bot.send_message(chat_id=message.chat.id, text=f'У вас {user_data["temp_cart"]["bonus"]} боунсов\nС каждой покупки вам начисляется 5% с потраченной суммы!', reply_markup=main_games_keyboard())


@bot.message_handler(regexp='^(Выиграй еще больше бонусов в рулетку!)$')
@bot.callback_query_handler(func=lambda call: call.data == 'roulette_finish')
def games_main(message):
    try:
        user_id = message.chat.id
    except AttributeError:
        user_id = message.message.chat.id
        bot.delete_message(user_id, message.message.message_id)
    bot.send_message(chat_id=user_id, text='Правила очень просты, угадаешь за какой кнопкой лежит приз,'
                                                   'удвоишь поставленную сумму, играем?', reply_markup=game_yes_no())


@bot.callback_query_handler(func=lambda call: call.data.split('|')[0] == 'roulette' and call.data.split('|')[1] in ['yes', 'no'])
def roulette(call):
    '''Главный хендлер игры в рулетку'''
    user_id = call.message.chat.id
    bot.delete_message(user_id, call.message.message_id)
    user_data = get_user(user_id)
    if call.data.split('|')[1] == 'yes':
        message = bot.send_message(user_id, f"У вас {user_data['temp_cart']['bonus']} бонусов!\n Введите сумму вашей ставки: ", reply_markup=cancel_keyboard())
        bot.register_next_step_handler(message, set_rate)
    else:
        bot.delete_message(user_id, call.message.message_id)


def set_rate(message):
    '''Задает ставку'''
    user_id = message.chat.id
    if message.text is not None:
        try:
            rate = int(message.text)
        except:
            message = bot.send_message(user_id, f"Введите сумму вашей ставки:", reply_markup=cancel_keyboard())
            bot.register_next_step_handler(message, set_rate)
            return
        if rate <= 0:   # Если ставка меньше 0
            message = bot.send_message(user_id, f"Ставка не может быть равна или меньше 0: ", reply_markup=cancel_keyboard())
            bot.register_next_step_handler(message, set_rate)
            return
        user_data = get_user(user_id)
        if rate > user_data['temp_cart']['bonus']:  # Если ставка больше баланса
            message = bot.send_message(user_id, f"Ставка не может быть больше вашего баланса: ", reply_markup=cancel_keyboard())
            bot.register_next_step_handler(message, set_rate)
            return
        global temp_data
        temp_data[user_id] = {'rate': rate}
        negative_num = -1 * rate
        set_rate_db(user_id, negative_num)
        return lvl_games(message)
    else:
        message = bot.send_message(user_id, f"Введите сумму вашей ставки:", reply_markup=cancel_keyboard())
        bot.register_next_step_handler(message, set_rate)


def lvl_games(message):
    '''Задает сложность игры (6,9,12 кнопок)'''
    user_id = message.chat.id
    bot.send_message(user_id, f"Выберите сложность: ", reply_markup=lvl_keyboard())


@bot.callback_query_handler(func=lambda call: call.data.split('|')[0] == 'roulette_lvl')
def roulette_games(call):
    '''Показывает список закрытых кнопок'''
    user_id = call.message.chat.id
    bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
    lvl = call.data.split('|')[1]
    bot.delete_message(user_id, call.message.message_id)
    keyboard, key_list = encode_roulette_keyboard(int(lvl))
    global temp_data
    temp_data[user_id]['key_list'] = key_list
    temp_data[user_id]['lvl'] = lvl
    rate = temp_data[user_id]['rate']
    bot.send_message(user_id, text=f'Ваша ставка {rate}\nВыберите из списка ниже: ', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data.split('|')[0] == 'roulette' and call.data.split('|')[1] in ['none', 'prize'])
def answer_roulette_games(call):
    '''Показывает список открытых кнопок'''
    user_id = call.message.chat.id
    global temp_data
    key_list, rate, lvl = temp_data[user_id]['key_list'], temp_data[user_id]['rate'], int(temp_data[user_id]['lvl'])
    keyboard = decode_roulette_keyboard(key_list)
    bot.delete_message(user_id, call.message.message_id)
    if call.data.split('|')[1] == 'prize':
        if lvl == 6:
            prize = int(rate + (rate * 0.5))
        elif lvl == 9:
            prize = int(rate + (rate * 1))
        elif lvl == 12:
            prize = int(rate + (rate * 2))
        set_prize_bonus(user_id, prize)
        user_data = get_user(user_id)
        bot.send_message(call.message.chat.id, text=f'Вы выиграли\nВаш баланс: {user_data["temp_cart"]["bonus"]}', reply_markup=keyboard)
        temp_data[call.message.chat.id] = None
    elif call.data.split('|')[1] == 'none':
        user_data = get_user(user_id)
        bot.send_message(call.message.chat.id, text=f'Вы проиграли\nВаш баланс: {user_data["temp_cart"]["bonus"]}', reply_markup=keyboard)
        temp_data[call.message.chat.id] = None
