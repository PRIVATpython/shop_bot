from db.db import db
from db import get_user


def set_default_temp_cart(user_id):
    db.users.update_one({'user_id': user_id}, {'$set': {'temp_cart.product': '', 'temp_cart.count': 1, 'temp_cart.price': 1, 'temp_cart.all_price': 0, 'category': ''}})

def give_bonus(user_id):
    user_data = db.users.find_one({'user_id': user_id})
    temp_cart = user_data['temp_cart']
    new_bonus = int((temp_cart['all_price'])/100*5)
    db.users.update_one({'user_id': user_id}, {'$set': {'temp_cart.product': '', 'temp_cart.count': 1, 'temp_cart.price': 1, 'temp_cart.all_price': 0, 'category': ''},
                                               '$inc': {'temp_cart.bonus': new_bonus}})

def get_bonus(user_id):
    user_data = db.users.find_one({'user_id': user_id})
    if user_data['temp_cart']['all_price'] > user_data['temp_cart']['bonus']:
        new_price = user_data['temp_cart']['all_price'] - user_data['temp_cart']['bonus']
        db.users.update_one({'user_id': user_id}, {'$set': {'temp_cart.all_price': new_price, 'temp_cart.bonus': 0}})
    else:
        new_bonus = user_data['temp_cart']['bonus'] - user_data['temp_cart']['all_price']
        db.users.update_one({'user_id': user_id}, {'$set': {'temp_cart.all_price': 1, 'temp_cart.bonus': new_bonus}})

def set_count_temp_cart(user_id, service, count, category):
    """изменяет кол-во в корзине"""
    user = get_user(user_id)
    user_count = user['temp_cart']['count']
    set_temp_cart(user_id, service, category)
    online_service_count = len(service['accounts'])
    if count < 0:
        if user_count + count <= 0:
            db.users.update_one({'user_id': user_id}, {'$set': {'temp_cart.count': 1, 'temp_cart.all_price': service['price'] * 1}})

            return False
    else:

        if user_count + count > online_service_count:
            db.users.update_one({'user_id': user_id}, {'$set': {'temp_cart.count': online_service_count, 'temp_cart.all_price': service['price'] * online_service_count}})
            return True
    db.users.update_one({'user_id': user_id}, {'$inc': {'temp_cart.count': count}})
    user_data = db.users.find_one({'user_id': user_id})
    print(service['price'] * user_data['temp_cart']['count'])
    db.users.update_one({'user_id': user_id}, {'$set': {'temp_cart.all_price': service['price'] * user_data['temp_cart']['count']}})


def set_temp_cart(user_id, service, category):
    """Задает сервис во временную корзину"""
    price = service['price']
    user_data = db.users.find_one({'user_id': user_id})
    if user_data['temp_cart']['all_price'] >= price:
        db.users.update_one({'user_id': user_id}, {'$set': {'temp_cart.product': service['name'],
                                                            'temp_cart.price': price,
                                                            'temp_cart.category': category}})
        return
    db.users.update_one({'user_id': user_id}, {'$set': {'temp_cart.product': service['name'],
                                                        'temp_cart.price': price,
                                                        'temp_cart.category': category,
                                                        'temp_cart.all_price': price}})

def get_temp_cart(user_id):
    user = db.users.find_one({'user_id': user_id})
    temp_cart = user['temp_cart']
    return temp_cart