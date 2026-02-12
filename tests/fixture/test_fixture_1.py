import time

from datetime import datetime
import pytest


@pytest.fixture
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
    return file

def test_text_write(textfile):
    # пишем текст
    textfile.write("hello world")