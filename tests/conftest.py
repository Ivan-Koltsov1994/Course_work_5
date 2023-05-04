import pytest, json
from classes.hh import HH

@pytest.fixture()
def hh():
    hh = HH(6)
    return hh
