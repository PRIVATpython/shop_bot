from db.db import db


def set_rate_db(user_id, rate):
     '''Отнимает сумму ставки от бонусов'''
     db.users.update_one({"user_id":user_id}, {'$inc': {"temp_cart.bonus": rate}})


def set_prize_bonus(user_id, prize):
     '''Прибавляет бонусы в случае победы'''
     db.users.update_one({"user_id": user_id}, {'$inc': {"temp_cart.bonus": prize}})