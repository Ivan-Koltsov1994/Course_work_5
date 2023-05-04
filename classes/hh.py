# Добавляем требуемые импорты
import requests
from datetime import datetime


class HH:
    """Класс для работы с сайтом HH"""

    URL = 'https://api.hh.ru/vacancies'  # Базовый URL для скачивания данных о вакансии

    def __init__(self, job: str):
        """Инициализируется запросом пользователя"""
        self.job = job
        self.par = {'text': f'{self.job}', 'page': 0, 'per_page': 100}  # Инициализируем данные по
        # названию профессии, id региона в HH, выводим количество страниц

    def __str__(self):
        return f'{self.job}'

    def __repr__(self):
        return f'Данные о вакансии: {self.job}'

    @staticmethod
    def get_formatted_date_hh(date: str) -> str:
        """Возвращает отформатированную дату"""
        date_format = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S+%f").strftime("%d.%m.%Y %X")
        return date_format

    def get_request(self):
        """Метод, позволяющий запросить данные о вакансий через API и требуемые параметры"""
        try:
            response = requests.get(self.URL, self.par)
            if response.status_code == 200:
                return response.json(), 'INFO:Данные получены успешно'
            return None, f'ERROR:status_code:{response.status_code} \n'

        except requests.exceptions.JSONDecodeError:
            return None, 'ERROR:requests.exceptions.JSONDecodeError \n'

        except requests.exceptions.ConnectionError:
            return None, 'ERROR:requests.exceptions.ConnectionError \n'

    def vacancy_info(self, data):
        """Метод, позволяющий получать данные о вакансии в требуемом виде (для ЗП в Рублях)"""

        info = {
            'source': 'HeadHunter',
            'name': data['name'],
            'url': data['alternate_url'],
            'description': data.get('snippet').get('responsibility'),
            'salary': data['salary'],
            'date_published': self.get_formatted_date_hh(data['published_at']),
            'area': data['area']['name']
        }
        return info

    def get_vacancies_list(self) -> list:
        """Метод, позволяющий положить данные о вакансиях в словарь"""
        vacancy_list_rus = []  # Массив с вакансиями c ЗП в рублях
        page = 0
        print("Ищем требуемые вакансии..")

        while True:
            self.par['page'] = page
            data = self.get_request()[0]

            for vacancy in data.get('items'):

                if vacancy.get('salary') == "RUR":
                    vacancy_list_rus.append(self.vacancy_info(vacancy))

                else:
                    vacancy_list_rus.append(self.vacancy_info(vacancy))

            if len(vacancy_list_rus) >= 500:
                break  # Прекращаем поиск при превышении длины списков в 500 позиций

            else:
                page += 1

        return vacancy_list_rus
