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
                'bonus': 0,
                'comment_pay': ''
                # добавить pay comment
            },
            "buy": []
        }
        db.users.insert_one(user)
    return user


def get_user(user_id):
    user = db.users.find_one({'user_id': user_id})
    return user


import datetime

def test():
    today = datetime.datetime.today()
    past = today + datetime.timedelta(days=-1)
    data = {'time': past, 'count': 10}
    x = db.test.find_one({'id': 'e3daf'})
    count = 0
    for i in x['statistic']:
        count += i['count']
    # db.test.update_one({'id': 'e3daf'}, {"$push": {'statistic': data}})

if __name__ == '__main__':
    test()