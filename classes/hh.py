# Делаем требуемые импорты
import requests
import time
from datetime import datetime

class HH:
    """Класс для работы с сайтом HH"""

    URL = 'https://api.hh.ru/vacancies'# Базовый URL для скачивания данных о вакансии

    def __init__(self, id: int):
        self.id = id
        self.params = {'employer_id': f'{self.id}', 'page': 0, 'per_page': 100}

    def get_request(self):
        """Метод, позволяющий запросить данные о вакансий через API и требуемые параметры"""
        try:
            response = requests.get(self.URL, self.params)
            if response.status_code == 200:
                return response.json(), 'INFO:Данные получены успешно'
            return None, f'ERROR:status_code:{response.status_code} \n'

        except requests.exceptions.JSONDecodeError:
            return None, 'ERROR:requests.exceptions.JSONDecodeError \n'

        except requests.exceptions.ConnectionError:
            return None, 'ERROR:requests.exceptions.ConnectionError \n'

    @staticmethod
    def get_formatted_date_hh(date: str) -> str:
        """Возвращает отформатированную дату"""
        date_format = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S+%f").strftime("%d.%m.%Y %X")
        return date_format


    def get_info(self,data: dict):
        """Метод, позволяющий получать данные о вакансии в требуемом виде (кортеж)"""
        vacancy_id = int(data.get('id'))
        vacancy_name = data['name']
        employer_id = int(data.get('employer').get('id'))
        city = data.get('area').get('name')
        url = data.get('alternate_url')
        data_published = self.get_formatted_date_hh(data.get('published_at'))

        if 'salary' in data.keys():
            if data.get('salary') is not None:
                if 'from' in data.get('salary'):
                    salary = data.get('salary').get('from')
                else:
                    salary = None
            else:
                salary = None
        else:
            salary = None

        vacancy = (vacancy_id, vacancy_name, employer_id, city, salary, url, data_published)

        return vacancy

    def get_vacancies(self) -> list:
        """Метод, позволяющий положить данные о вакансиях """
        vacancies = []
        page = 0
        while True:
            self.params['page'] = page
            data, info = self.get_request()

            for vacancy in data.get('items'):
                if vacancy.get('salary') is not None and vacancy.get('salary').get('currency') is not None:

                    # если зп рубли, добавляем в список, если нет, пропускаем
                    if vacancy.get('salary').get('currency') == "RUR":
                        vacancies.append(self.get_info(vacancy))
                    else:
                        continue

                # если зп не указана, добавляем в список
                else:
                    vacancies.append(self.get_info(vacancy))

            page += 1
            time.sleep(0.2)

            # если была последняя страница, заканчиваем сбор данных
            if data.get('pages') == page:
                break

        return vacancies

# hh= HH(6)
# print(hh.get_vacancies())