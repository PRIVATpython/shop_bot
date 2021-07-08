import random
import string
import requests
from settings import QIWI_TOKEN


def generate_alphanum_random_string(length):
    """Генератор рандомных строк типа - s4Knf3Lf35"""
    letters_and_digits = string.ascii_letters + string.digits
    rand_string = ''.join(random.sample(letters_and_digits, length))
    return rand_string


def generate_cd_key(count):
    """Генератор случайных ключей типа - gkF43-Hn2L2-pOi5t-4Nklp-0Jfkl"""
    key_list = []
    for i in range(count):
        key = f'{generate_alphanum_random_string(5)}-{generate_alphanum_random_string(5)}-{generate_alphanum_random_string(5)}-{generate_alphanum_random_string(5)}-{generate_alphanum_random_string(5)}'
        key_list.append(key)
    return key_list


def generator_normal_acc(count):
    """Генератор случайных логинов и паролей типа - VasyaPupkin34@yandex.ru|s4Knf3Lf35"""
    login_list = []
    for i in range(count):
        res = requests.get('http://api.randomdatatools.ru').json()
        login_data = f'{res["Email"]}|{res["Password"]}'
        login_list.append(login_data)
    return login_list


def get_pay_in(api_access_token):
    '''Берет последние 25 входящих платежей на киви'''
    s7 = requests.Session()
    s7.headers['Accept']= 'application/json'
    s7.headers['authorization'] = 'Bearer ' + api_access_token
    parameters = {'rows': 25, 'operation': "IN"}
    p = s7.get('https://edge.qiwi.com/payment-history/v2/persons/79006292609/payments', params = parameters)
    return p.json()


def check_qiwi_pay(comment, price):
    '''Проверяет платеж по коментарию и сумме'''
    payments = get_pay_in(QIWI_TOKEN)
    for payment in payments['data']:
        comment_pay = payment['comment']
        price_pay = payment['sum']['amount']
        if comment_pay == comment and price_pay == price:
            return True
    return False


