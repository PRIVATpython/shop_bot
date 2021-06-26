import requests
# from db.db import db

while True:
    x = requests.get('http://api.randomdatatools.ru').json()
    print(f'{x["Email"]}|{x["Password"]}')