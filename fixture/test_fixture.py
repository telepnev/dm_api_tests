import pytest


@pytest.mark.parametrize(
    "file_name, text", [
        ("file_1.txt", "Some_text_1"),
        ("file_2.txt", "Some_text_2"),
        ("file_3.txt", "Some_text_3"),

    ]
)
def test_write_file(file_name, text):
    with open(file_name, 'w') as f:
        f.write(text)
