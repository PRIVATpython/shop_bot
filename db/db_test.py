import requests


def generator_normal_acc(count):
    login_list = []
    for i in range(count):
        res = requests.get('http://api.randomdatatools.ru').json()
        login_data = f'{res["Email"]}|{res["Password"]}'
        login_list.append(login_data)
    return login_list
