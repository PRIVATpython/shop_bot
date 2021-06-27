from db.db import db
from db import get_temp_cart
import os

# DB----------------------------------------------------------------------------
def get_data_account_no_subcategory_keyboard(category):
    '''Достает информацию для кнопок покупки/онлайн сервисы'''
    services = db.online_service.find({"high_id": category, 'accounts': {'$type': 4, '$ne': []}})
    # services = db.online_service.find({'high_id': category})
    return services


def get_data_account_no_subcategory(service):
    '''Достает инофрмацию для товара покупки/онлайн сервисы'''

    service = db.online_service.find_one({'id': service})
    return service

def main_category_no_subcategory():
    category_raw = db.online_service.find()
    category = set()
    for item in category_raw:
        category.add(item['high_id'])
    return category

def main_category_no_subcategory_data():
    category_raw = db.online_service.find()
    category = {}
    for item in category_raw:
        category[item['high_id']] = item['name_category']
        # category.add(item['high_id'])
    return category

# admin_db----------------------------------------------------------------------------
def get_admin_data_no_subcategory(category):
    '''Достает информацию для кнопок покупки/онлайн сервисы'''
    services = db.online_service.find({'high_id': category})
    return services


def add_no_subcategory_account(callback, account):
    db.online_service.update({'id': callback}, {"$push": {'accounts': account}})


def add_new_no_subcategory(admin_data):
    db.online_service.insert_one(admin_data)
    service = db.online_service.find_one({'name': admin_data['name']})
    id = str(service['_id'])[-5:]
    db.online_service.update_one({'name': admin_data['name']},
                                 {'$set': {'id': id, 'callback': f'{admin_data["high_id"]}|{id}|None'}})


def del_no_subcategory_db(service):
    goods = db.online_service.find_one({'id': service})
    if goods['img'].split('/')[0] == 'img':
        os.remove(path=goods['img'])
    db.online_service.remove({'id': service})

# def change_online_service(dat, category, service):
#     db.online_service.update_one({'id': service}, {'$set': {category: dat}})

def change_no_subcategory(data, service, category):
    if category == 'img':
        goods = db.online_service.find_one({'id': service})
        if goods['img'].spilt('/')[0] == 'img':
            os.remove(path=goods['img'])
    db.online_service.update_one({'id': service}, {'$set': {category: data}})


def find_no_subcategory_name(high_id):
    category = db.online_service.find_one({'high_id': high_id})
    return category

def del_main_no_subcategory(high_id):
    db.online_service.remove({'high_id': high_id})

# give_account----------------------------------------------------------------------------
def give_account_no_subcategory(user_id):
    temp_cart = get_temp_cart(user_id)
    count = temp_cart['count']
    service = db.online_service.find_one({'name': temp_cart['product']})
    accounts_list = service['accounts']
    accounts = []
    for item in range(count):
        account = accounts_list.pop(0)
        accounts.append(account)
        db.online_service.update({'name': temp_cart['product']}, {'$set': {'accounts': accounts_list}})
    print(accounts_list)
    return accounts

