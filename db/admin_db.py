from db.db import db


def set_temp_data_admin(user_id, callback):
    db.users.update_one({'user_id': user_id}, {'$set': {'temp_data_admin': callback}})


