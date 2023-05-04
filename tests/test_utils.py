from utils.utils import read_json, get_employers


def test_get_employers():
    """Тестируем получение списка кортежей из списка словарей"""
    assert get_employers([{'id': 1, 'title': '1'}, {'id': 2, 'title': '2'}]), [(1, 1), (2, 2)]


def test_read_json():
    """Тестируем функцию для чтения json-файл"""
    assert isinstance(read_json("data/employers_base.json"), list)
