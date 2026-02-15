import pytest


@pytest.fixture(params=["1.txt", "2.txt"])
def text_file(request):
    file = open(request.param, "w")
    yield file


def test_text_file_write(text_file):
    text_file.write("hello")
