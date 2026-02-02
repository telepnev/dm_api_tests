from pprint import pprint
from json import loads

import requests


def test_post_v1_account():
    login = "tele_test_10"
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
    assert response.status_code == 201, f"Пользователь не был создан {response.text}"

    # Получить письма из почтового ящика
    params = {
        'limit': '50',
    }
    response = requests.get('http://185.185.143.231:5025/api/v2/messages', params=params, verify=False)
    print(response.status_code)
    assert response.status_code == 200, "Письмо не получено"

    token = None
    # Получить активационный токен
    for item in response.json()['items']:
        user_data = loads(item['Content']['Body'])
        user_login = user_data["Login"]

        if user_login == login:
            print(f"Login {user_login}")
            token = user_data.get("ConfirmationLinkUrl").split("/")[-1]

    assert token is not None, f"Токен для пользователя {login} не был получен"

    # Активация пользователя
    response = requests.put(f"http://185.185.143.231:5051/v1/account/{token}")
    print(response.status_code)
    assert response.status_code == 200, "Пользователь не активирован"

    # Авторизация
    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True,
    }

    response = requests.post('http://185.185.143.231:5051/v1/account/login', json=json_data)
    print(response.status_code)
    assert response.status_code == 200, "Пользователь не авторизован"

