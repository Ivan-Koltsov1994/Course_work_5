import pytest, json
from classes.hh import HH
from classes.dbManager import DBManager
from utils import config

@pytest.fixture()
def hh():
    hh = HH(6)
    return hh

@pytest.fixture
def db():
    params = config
    a = DBManager('tests', params)
    return a
