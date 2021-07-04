from telebot import types
import random


def main_games_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    roulette = types.KeyboardButton('Выиграй еще больше бонусов в рулетку!')
    bonus = types.KeyboardButton('Мои бонусы')
    back = types.KeyboardButton('Назад к главному меню')
    keyboard.add(roulette)
    keyboard.add(bonus)
    keyboard.add(back)
    return keyboard


def game_yes_no():
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text='Да', callback_data=f'roulette|yes'))
    keyboard.add(types.InlineKeyboardButton(text='Нет', callback_data=f'roulette|no'))
    return keyboard

def lvl_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text='Легко (Выигрыш x1.25 | Шанс 16%)', callback_data=f'roulette_lvl|6'))
    keyboard.add(types.InlineKeyboardButton(text='Cредне (Выигрыш x2 | Шанс 11%)', callback_data=f'roulette_lvl|9'))
    keyboard.add(types.InlineKeyboardButton(text='Сложно (Выигрыш x3 | Шанс 8%)', callback_data=f'roulette_lvl|12'))
    return keyboard

def encode_roulette_keyboard(lvl):
    """Рулетка"""
    list_key = []
    # Создаем список только с 1 призом
    for item in range(lvl-1):
        list_key.append('none')
    else:
        list_key.append('prize')
    # Хорошенько перемешиваем список
    for item in range(len(list_key) - 1, 0, -1):
        j = random.randint(0, item)
        list_key[item], list_key[j] = list_key[j], list_key[item]

    keyboard = types.InlineKeyboardMarkup()
    len_list = len(list_key)
    # В 1 ряду Inline клаивиатуры может уместится только 3 кнопки
    for item in range(0, len_list, 3):
        if len_list - item < 2:     # Если в последнем ряду остается только 1 кнопка
            button = types.InlineKeyboardButton(text=f'❓', callback_data=f"roulette|{list_key[item]}")
            keyboard.add(button)
        elif len_list - item < 3:   # Если в последнем ряду остается только 2 кнопки
            button = types.InlineKeyboardButton(text=f'❓', callback_data=f"roulette|{list_key[item]}")
            button1 = types.InlineKeyboardButton(text=f'❓', callback_data=f"roulette|{list_key[item + 1]}")
            keyboard.add(button, button1)
        else:   # Если в последнем ряду остается только 3 кнопки
            button = types.InlineKeyboardButton(text=f'❓', callback_data=f"roulette|{list_key[item]}")
            button1 = types.InlineKeyboardButton(text=f'❓', callback_data=f"roulette|{list_key[item + 1]}")
            button2 = types.InlineKeyboardButton(text=f'❓', callback_data=f"roulette|{list_key[item + 2]}")
            keyboard.add(button, button1, button2)
    return keyboard, list_key   # Возвращаем клавиатуру и перемешанный список для создания клавиатуры с ответами


def decode_roulette_keyboard(list_key):
    keyboard = types.InlineKeyboardMarkup()
    len_list = len(list_key)
    for item in range(0, len_list, 3):
        if len_list - item < 2:
            if list_key[item] == 'yes':
                text = '✅'
            else:
                text = '❌'
            button = types.InlineKeyboardButton(text=text, callback_data=f"roulette_finish")
            keyboard.add(button)

        elif len_list - item < 3:
            answer_list = []
            if list_key[item] == 'prize':
                text = '✅'
                answer_list.append(text)
            else:
                text = '❌'
                answer_list.append(text)

            if list_key[item+1] == 'prize':
                text = '✅'
                answer_list.append(text)
            else:
                text = '❌'
                answer_list.append(text)
            len_answer_list = len(answer_list)
            for h in range(0, len_answer_list, 2):
                button = types.InlineKeyboardButton(text=answer_list[h], callback_data=f"roulette_finish")
                button1 = types.InlineKeyboardButton(text=answer_list[h+1], callback_data=f"roulette_finish")
            keyboard.add(button, button1)

        else:
            answer_list = []
            if list_key[item] == 'prize':
                text = '✅'
                answer_list.append(text)
            else:
                text = '❌'
                answer_list.append(text)

            if list_key[item + 1] == 'prize':
                text = '✅'
                answer_list.append(text)
            else:
                text = '❌'
                answer_list.append(text)

            if list_key[item + 2] == 'prize':
                text = '✅'
                answer_list.append(text)
            else:
                text = '❌'
                answer_list.append(text)
            len_answer_list = len(answer_list)
            for h in range(0, len_answer_list, 3):
                button = types.InlineKeyboardButton(text=answer_list[h], callback_data=f"roulette_finish")
                button1 = types.InlineKeyboardButton(text=answer_list[h+1], callback_data=f"roulette_finish")
                button2 = types.InlineKeyboardButton(text=answer_list[h+2], callback_data=f"roulette_finish")
            keyboard.add(button, button1, button2)

    return keyboard