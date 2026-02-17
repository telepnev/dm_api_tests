import time
import pytest

from datetime import datetime
from pathlib import Path

"""
Когда используют session scope?

🔥 1. Подключение к БД
🔥 2. Авторизация через API (получение токена)
🔥 3. Поднятие браузера (иногда)
🔥 4. Чтение конфигурации
🔥 5. Тяжёлые ресурсы (docker, сервисы)
"""


@pytest.fixture(scope="session")
def textfile():
    # имитация длительности
    time.sleep(1)
    # получаем текущее дату и время
    now = datetime.now()
    # преобразование даты
    date = now.strftime("%Y-%m-%d_%H-%M-%S")
    # формируем название файла
    file_name = f"{date}.txt"
    file = open(file_name, "w")
    # return -> yield
    yield file
    file.close()
    # удаляем файл
    Path(file_name).unlink()


def test_text_write(textfile):
    # пишем текст
    textfile.write("hello world - test_text_write")


def test_text_write_2(textfile):
    # пишем текст
    textfile.write("hello world - test_text_write_2")


def test_text_write_3(textfile):
    # пишем текст
    textfile.write("hello world - test_text_write_3")


"""
в нашем случаи все тесты записали результат в один файл
"""
