import random
import string
import requests


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





