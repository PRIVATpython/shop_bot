from . import db


def purch_product(user_id):
    '''Генерит информацию для клавиатуры моих покупок'''
    category_raw = db.users.find_one({"user_id": user_id})
    category_raw = category_raw['buy']
    category = {}
    for i in category_raw:
        category[i['name']] = i['callback']
    return category


def purch_accounts(user_id, service_id):
    '''Выдает инофрмацию по купленным юзером аккаунтам'''
    service = db.users.find_one({"user_id": user_id, "buy.id":service_id}, {"buy.$": 1})
    service = service['buy'][0]
    return service