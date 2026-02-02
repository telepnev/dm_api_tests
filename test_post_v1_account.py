import requests


def test_post_v1_account():
    login = "tele_test_3"
    email = f"{login}@mail.com"
    password = "12345678"


    # Регистрация пользователя
    json_data = {
        'login': login,
        'email': email,
        'password': password,
    }


    response = requests.post('http://185.185.143.231:5051/v1/account', json=json_data)
    print(response.status_code)
    print(response.text)

    # Получить письма из почтового ящика
    params = {
        'limit': '50',
    }
    response = requests.get('http://185.185.143.231:5025/api/v2/messages', params=params, verify=False)
    print(response.status_code)
    print(response.text)

    # Получить активационный токен

    # Активация пользователя

    response = requests.put('http://185.185.143.231:5051/v1/account/10af8997-6b3a-41b5-a975-c514b320f063')
    print(response.status_code)
    print(response.text)
    # Авторизация

    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True,
    }

    response = requests.post('http://185.185.143.231:5051/v1/account/login', json=json_data)
    print(response.status_code)
    print(response.text)
