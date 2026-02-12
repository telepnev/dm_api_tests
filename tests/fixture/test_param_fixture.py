import pytest


@pytest.fixture(params=["1.tx", "2.tx"])
def textfile(request):
    file = open(request.param, "w")
    return file

def test_parametrized_fixture(textfile):
    textfile.write("hello world from parametrized_fixture")