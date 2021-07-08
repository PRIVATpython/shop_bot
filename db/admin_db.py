from db.db import db


def set_temp_data_admin(user_id, callback):
    '''Задает callback в БД, для создания новых товаров/подкатегорий'''
    db.users.update_one({'user_id': user_id}, {'$set': {'temp_data_admin': callback}})


def get_users_admin():
    '''Находит всех администраторов'''
    admins = db.users.find({'admin': 'admin'})
    return admins


def del_admin_db(user_id):
    '''Удаляет выбраного администратора'''
    db.users.update_one({'user_id': user_id}, {'$set': {'admin': None}})


def add_admin_db(username):
    '''Добавляет администратора'''
    user = db.users.find_one({'username': username})
    if user is None:
        return False
    else:
        db.users.update_one({'username': username}, {'$set': {'admin': 'admin'}})
        return True