from db.db import db
from db import get_temp_cart
import os
import datetime


def get_data_account_no_subcategory_keyboard(category):
    '''No Subcategory - Достает информацию только не пустого товара'''
    services = db.online_service.find({"high_id": category, 'accounts': {'$type': 4, '$ne': []}})
    return services


def get_data_account_no_subcategory(service):
    '''No Subcategory - Достает инофрмацию товара'''
    service = db.online_service.find_one({'id': service})
    return service


def main_category_no_subcategory():
    '''No Subcategory - множество id главных катеогрий'''
    category_raw = db.online_service.find()
    category = set()
    for item in category_raw:
        category.add(item['high_id'])
    return category


def main_category_no_subcategory_data():
    """No Subcategory - Для клавиатуры"""
    category_raw = db.online_service.find()
    category = {}
    for item in category_raw:
        category[item['high_id']] = item['name_category']
    return category

# admin_db----------------------------------------------------------------------------


def get_admin_data_no_subcategory(category):
    '''Находит все гланвые категории в No subcategory'''
    services = db.online_service.find({'high_id': category})
    return services


def add_no_subcategory_account(callback, account):
    '''Добавляет новые аккаунты в существующий товар'''
    db.online_service.update({'id': callback}, {"$push": {'accounts': account}})


def add_new_no_subcategory(admin_data):
    '''Добавляет новый товар'''
    db.online_service.insert_one(admin_data)
    service = db.online_service.find_one({'name': admin_data['name']})
    id = str(service['_id'])[-5:]
    db.online_service.update_one({'name': admin_data['name']},
                                 {'$set': {'id': id, 'callback': f'{admin_data["high_id"]}|{id}|None'}})


def del_no_subcategory_db(service):
    '''Удаляет товар'''
    goods = db.online_service.find_one({'id': service})
    if goods['img'].split('/')[0] == 'img':
        os.remove(path=goods['img'])
    db.online_service.remove({'id': service})


def change_no_subcategory(data, service, category):
    '''Изменяет цену/описание/фото товара'''
    if category == 'img':
        goods = db.online_service.find_one({'id': service})
        if goods['img'].spilt('/')[0] == 'img':
            os.remove(path=goods['img'])
    db.online_service.update_one({'id': service}, {'$set': {category: data}})


def find_no_subcategory_name(high_id):
    '''Находит имя главной катеогрии по id'''
    category = db.online_service.find_one({'high_id': high_id})
    return category


def del_main_no_subcategory(high_id):
    '''Удаляет все товары выбранной главной категории'''
    db.online_service.remove({'high_id': high_id})

def change_main_category_no_sub(old_name, new_name):
    '''Изменяет имя главной категории'''
    db.online_service.update_many({"name_category": old_name}, {"$set": {"name_category": new_name}})


def show_statistic_no_sub(period, service_id):
    '''Показывает статистику товара''' # За сутки не показывает товаров
    today = datetime.datetime.today()
    past = today + datetime.timedelta(days=-period)
    service = db.online_service.find_one({'id': service_id})
    statistic = service['statistic']
    count = 0
    sum = 0
    for item in statistic:
        if item['date'] < past:
            break
        count += len(item['accounts'])
        sum += item['sum']
    return count, sum

# give_account----------------------------------------------------------------------------


def give_account_no_subcategory(user_id):
    '''Отдает аккаунты пользователю после успешной покупки'''
    temp_cart = get_temp_cart(user_id)
    count = temp_cart['count']
    service = db.online_service.find_one({'name': temp_cart['product']})
    accounts_list = service['accounts']
    accounts = []
    for item in range(count):
        account = accounts_list.pop(0)
        accounts.append(account)
        db.online_service.update({'name': temp_cart['product']}, {'$set': {'accounts': accounts_list}})
    statistic_no_sub(user_id=user_id, accounts=accounts, service_id=service['id'], sum=temp_cart['all_price'])
    my_purchases_no_sub(service['name'], user_id, accounts)
    return accounts


def statistic_no_sub(user_id, accounts, service_id, sum):
    '''Записывает статистику после покупки'''
    today = datetime.datetime.today()
    data = {
        'user_id': user_id,
        "accounts": accounts,
        "date": today,
        "sum": sum
    }
    db.online_service.update_one({'id': service_id}, {"$push": {'statistic': data}})


def my_purchases_no_sub(service, user_id, accounts):
    '''Добавляет аккаунты в список покупок пользователя после покпки'''
    service_data = db.online_service.find_one({"name": service})
    del service_data['_id']
    del service_data['img']
    del service_data['description']
    del service_data['price']
    del service_data['name_category']
    del service_data['high_id']
    service_data['accounts'] = []
    service_data['callback'] = f'purch|{service_data["id"]}'
    user_data = db.users.find_one({'user_id': user_id, 'buy.id': service_data['id']})
    if user_data is None:
        db.users.update_one({'user_id': user_id}, {'$push': {'buy': service_data}})
    for item in accounts:
        db.users.update_one({'user_id': user_id}, {'$push': {'buy.$[i].accounts': item}}, array_filters=[{"i.id": service_data['id']}])