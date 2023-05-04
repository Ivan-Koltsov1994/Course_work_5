from classes.hh import HH


def test_hh_str(hh):
    """Тестируем метод __str__класса HH"""
    assert hh.__str__() == '6'

def test_hh_repr(hh):
    """Тестируем метод __repr__класса HH"""
    assert hh.__repr__() == "Данные о работодателе с id: 6"

def test_get_formatted_date_hh():
    """Тестируем ожидаемое поведение при форматировании даты"""
    assert HH.get_formatted_date_hh('2023-03-13T07:54:44+0300') == '13.03.2023 07:54:44'

def test_get_request_hh(hh):
    """Тестируем что метод get_request класса HH возвращает данные"""
    assert hh.get_request() is not None
    assert type(hh.get_request()) is tuple
    data,info = hh.get_request()
    assert info == ('INFO:Данные получены успешно')

def test_get_request_error_hh(hh):
    """Тестируем ошибки метода get_request класса HH"""
    HH.URL = 'https://api.hh.ru/vacancie!!'
    assert hh.get_request() == (None, 'ERROR:status_code:404 \n')

def test_get_info(hh):
    """Ожидается получение информации о вакансии в нужном формате"""

    assert hh.get_vacancies() is not None
    assert isinstance(hh.get_vacancies(), list)