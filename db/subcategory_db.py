from db.db import db
from db import get_temp_cart
from utilites import generate_alphanum_random_string
import os
import datetime


#db-----------------------------------------------------------
def get_category_subcategory(cat):
    '''Находит все главные категории'''
    social_network = db.social_network.find({'high_id': cat})
    return social_network


def get_subcategory(category):
    '''Находит подкатеогрию '''
    social_network = db.social_network.find_one({'id': category})
    return social_network


def get_subcategory_data(callback):
    '''Выдает массив с информацией о товаре'''
    social_network = db.social_network.find_one({"accounts_data.id": callback},  {"accounts_data.$" : 1})
    social_network = social_network['accounts_data'][0]
    return social_network


def main_category_subcategory():
    '''Выдает множество id главных категорий'''
    category_raw = db.social_network.find()
    category = set()
    for item in category_raw:
        category.add(item['high_id'])
    return category


def main_category_subcategory_data():
    '''Находит имя всех гланых категорий'''
    category_raw = db.social_network.find()
    category = {}
    for item in category_raw:
        category[item['high_id']] = item['name_category']
    return category


def find_cat_name(high_id):
    category = db.social_network.find_one({'high_id': high_id})
    return category

#admin_db-----------------------------------------------------------


def add_subcategory_account(callback, account):
    '''Добавляет аккаунты в существующий товар'''
    db.social_network.update_one({"accounts_data.id": callback}, {'$push': {"accounts_data.$.accounts": account}})


def add_subcategory(admin_data):
    '''Добавляет новый товар'''
    id = generate_alphanum_random_string(5)     # Возможно будет проще сделать id от
    accounts_data = {
            'name': admin_data['name'],
            'price': int(admin_data['price']),
            'callback': f'{admin_data["category"]}|{admin_data["high_id"]}|{id}|None|None',
            'description': admin_data['description'],
            'accounts': [],
            'img': admin_data['img'],
            'id': id,
            'statistic': []
        }

    high_id = admin_data['high_id']
    service = db.social_network.find_one({'id': high_id})
    db.social_network.update_one({"id": high_id}, {'$push': {"accounts_data": accounts_data}})


def add_new_cat_subcategory(admin_data):
    '''Добавляет новую подкатегорию'''
    category_data = {
        'name': admin_data['name'],
        'img': admin_data['img'],
        'callback': '',
        'accounts_data': [],
        'id': '',
        'high_id': admin_data['high_id'],
        'name_category': admin_data['name_category']
    }
    db.social_network.insert(category_data)
    category = db.social_network.find_one({'name': admin_data['name']})
    id = str(category['_id'])[-5:]
    db.social_network.update_one({'name': admin_data['name']},
                                 {'$set': {'id': id, 'callback': f'{admin_data["high_id"]}|{id}|None|None|None'}})


def del_subcategory(id, service):
    '''Удаляет товар'''
    social_network = db.social_network.find_one({"accounts_data.id": service},  {"accounts_data.$" : 1})   # исправить выдачу определенного массива, а не всего документа
    img = social_network['accounts_data'][0]['img']
    if img.split('/')[0] == 'img':
        os.remove(path=img)
    db.social_network.update_one({'id': id}, {'$pull': {'accounts_data': {'id': service}}})


def del_cat_subcategory(service):
    '''Удаляет подкаетогрию'''
    category = db.social_network.find_one({'id': service})
    if category['img'].split('/')[0] == 'img':
        os.remove(path=category['img'])
    db.social_network.remove({'id': service})


def change_cat_subcategory(url_photo, category, service):
    '''Изменяет подкатегорию'''
    db.social_network.update_one({'id': service}, {'$set': {category: url_photo}})


def change_good_subcategory(data, category, service):
    '''Изменяет товар'''
    db.social_network.update_one({"accounts_data.id": service}, {'$set': {f"accounts_data.$.{category}": data}})


def del_main_category(high_id):
    '''Удаляет подкатегорию'''
    db.social_network.remove({'high_id': high_id})

def change_main_category_sub(old_name, new_name):
    '''Изменяет имя главной категории'''
    db.social_network.update_many({"name_category": old_name}, {"$set": {"name_category": new_name}})


#give_account-----------------------------------------------------------


def give_account_subcategory(user_id):
    '''Выдает аккаунты пользователю после успешной покупки'''
    temp_cart = get_temp_cart(user_id)
    count = temp_cart['count']
    service = db.social_network.find_one({"accounts_data.name": temp_cart['product']}, {"accounts_data.$": 1})
    accounts_list = service['accounts_data'][0]['accounts']
    accounts = []
    for item in range(count):
        account = accounts_list.pop(0)
        accounts.append(account)
        db.social_network.update_one({"accounts_data.name": temp_cart['product']}, {'$set': {"accounts_data.$.accounts": accounts_list}})
    statistic_sub(user_id=user_id, accounts=accounts, service_id=service['accounts_data'][0]['id'])
    my_purchases(temp_cart['product'], user_id, accounts)
    return accounts

def statistic_sub(user_id, accounts, service_id):
    '''Заносит купленные аккаунты,user_id и сумму в БД в статистику'''
    today = datetime.datetime.today()
    data = {
        'user_id': user_id,
        "accounts": accounts,
        "date": today
    }
    db.social_network.update_one({"accounts_data.id": service_id}, {'$push': {f"accounts_data.$.statistic": data}})


def my_purchases(service, user_id, accounts):
    '''Заносит купленные аккаунты в список покупок'''
    product_data = db.social_network.find_one({"accounts_data.name": service}, {"accounts_data.$": 1})
    product_data = product_data['accounts_data'][0]
    del product_data['price']
    del product_data['description']
    del product_data['img']
    product_data['accounts'] = []
    product_data['callback'] = f'purch|{product_data["id"]}'
    user_data = db.users.find_one({'user_id': user_id, 'buy.id': product_data['id']})
    if user_data is None:
        db.users.update_one({'user_id': user_id}, {'$push': {'buy': product_data}})
    for item in accounts:
        db.users.update_one({'user_id': user_id}, {'$push': {'buy.$[i].accounts': item}}, array_filters=[{"i.id": product_data['id']}])