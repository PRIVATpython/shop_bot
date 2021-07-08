from pymongo import MongoClient
from settings import MONGO_DB_LINK, MONGO_DB

client = MongoClient(MONGO_DB_LINK)
db = client[MONGO_DB]


def get_or_create_user(user_data):
    '''Создание/получение юзера'''
    user = db.users.find_one({'user_id': user_data.id})
    if user :
        if user['username'] != user_data.username:
            db.users.update_one({'user_id': user_data.id}, {'$set': {'username': user_data.username}})
    elif not user:
        user = {
            "user_id": user_data.id,
            "first_name": user_data.first_name,
            "admin": None,
            "last_name": user_data.last_name,
            "username": user_data.username,
            "temp_cart": {
                'product': '',
                'price': 1,
                'count': '',
                'category': '',
                'bonus': 0,
                'comment_pay': ''
            },
            "buy": []
        }
        db.users.insert_one(user)
    return user


def get_user(user_id):
    '''Получение юзера по id'''
    user = db.users.find_one({'user_id': user_id})
    return user

