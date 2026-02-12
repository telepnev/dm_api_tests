from pathlib import Path

import pytest


@pytest.mark.parametrize("file_name", ["file_name_1.txt", "file_name_2.txt", "file_name_3.txt"])
def test_text_write(file_name):
    # пишем текст
    with open(file_name, "w") as file:
        file.write("hello world - test_text_write")
        file.close()
        Path(file_name).unlink()


@pytest.mark.parametrize(
    "file_name, text", [
        ("file_name_1.txt", "hello world - test_text_write file_name_1"),
        ("file_name_2.txt", "hello world - test_text_write file_name_2"),
        ("file_name_3.txt", "hello world - test_text_write test_text_write file_name_3"),
    ])
def test_write_to_file(file_name, text):
    with open(file_name, "w") as file:
        file.write(text)
        file.close()
        Path(file_name).unlink()
