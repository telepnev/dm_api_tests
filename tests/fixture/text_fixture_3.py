import time
import pytest

from datetime import datetime
from pathlib import Path


@pytest.fixture(scope="function")
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
