from pymongo import MongoClient
from settings import MONGO_DB_LINK, MONGO_DB

client = MongoClient(MONGO_DB_LINK)
db = client[MONGO_DB]


def get_or_create_user(user_data):
    '''Создание/получение юзера'''
    user = db.users.find_one({'user_id': user_data.id})
    if not user:
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
                'bonus': 0
            },
            "buy": []
        }
        db.users.insert_one(user)
    return user


def get_user(user_id):
    user = db.users.find_one({'user_id': user_id})
    return user

#TEST-------------------------------------------------
def add_test(high_id):
    x = db.social_network.find_one({'high_id': high_id})
    return x

if __name__ == '__main__':
    x = add_test('social')


