# Добавляем требуемые импорты
import psycopg2
from psycopg2 import errors


class DBManager:
    """Класс для работы с базой данных"""
    def __init__(self, dbname: str, params: dict):
        self.dbname = dbname # Инициализируемся по имени базы данных
        self.params = params # Параметры базы данных

    def __str__(self):
        return f'{self.dbname}'

    def __repr__(self):
        return f'Работаем с таблицей: {self.dbname}'

    def create_database(self):
        """Метод создает базу данных и таблицы для сохранения данных"""

        # Делаем подключение к базе данных
        conn = psycopg2.connect(dbname='postgres', **self.params)
        conn.autocommit = True # Автокоммит SQL-запросов
        cur = conn.cursor()

        try:
            cur.execute(f"DROP DATABASE IF EXISTS {self.dbname}")
            cur.execute(f"CREATE DATABASE {self.dbname}")

        except psycopg2.errors.ObjectInUse:
            # Проверяем, что если было активное подключение, удаляет его, удаляет БД и создает ее заново
            cur.execute("SELECT pg_terminate_backend(pg_stat_activity.pid) "
                        "FROM pg_stat_activity "
                        f"WHERE pg_stat_activity.datname = '{self.dbname}' ")
            cur.execute(f"DROP DATABASE IF EXISTS {self.dbname}")
            cur.execute(f"CREATE DATABASE {self.dbname}")
            print('Было активное подключение к базе данных, мы его удалили\n .................................')

        finally:
            # Закрываем курсор и коннект к БД
            cur.close()
            conn.close()

        #  Подключаемся к созданной БД и создаем таблицы
        conn = psycopg2.connect(dbname=self.dbname, **self.params)
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute('CREATE TABLE IF NOT EXISTS employers '
                                '('
                                'employer_id int PRIMARY KEY, '
                                'employer_name varchar(255) UNIQUE NOT NULL)')

                    cur.execute('CREATE TABLE IF NOT EXISTS vacancies '
                                '('
                                'vacancy_id int PRIMARY KEY, '
                                'vacancy_name varchar(255) NOT NULL, '
                                'employer_id int REFERENCES employers(employer_id) NOT NULL, '
                                'area varchar(255), '
                                'url text, '
                                'salary int,'
                                'date_published timestamp,'
                                'source text)')
        finally:
            conn.close()

    def insert_data(self, table_name: str, data: list) -> None:
        """Метод добавляет данные в базу данных в зависимости от таблицы"""

        conn = psycopg2.connect(dbname=self.dbname, **self.params)

        try:
            with conn:
                with conn.cursor() as cur:
                    if table_name == 'employers':
                        cur.executemany('INSERT INTO employers(employer_id, employer_name) '
                                        'VALUES(%s, %s)', data)
                    elif table_name == 'vacancies':
                        cur.executemany('INSERT INTO vacancies (vacancy_id, vacancy_name, employer_id, '
                                        'area,  url, salary, date_published, source) '
                                        'VALUES(%s, %s, %s, %s, %s, %s)'
                                        'ON CONFLICT (vacancy_id) DO NOTHING', data)
                    else:
                        print("Такой таблицы не существует.")
        finally:
            conn.close()

    def _execute_query(self, query) -> list:
        """Метод возвращает результаты запроса и возвращает список кортежей"""
        conn = psycopg2.connect(dbname=self.dbname, **self.params)
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute(query)
                    result = cur.fetchall()

        finally:
            conn.close()

        return result

    def get_companies_and_vacancies_count(self) -> list:
        """Метод получает список всех компаний и количество вакансий у каждой компании."""
        result = self._execute_query("SELECT employer_name, COUNT(*) as total_vacancies "
                                     "FROM vacancies "
                                     "LEFT JOIN employers USING(employer_id)"
                                     "GROUP BY employer_name "
                                     "ORDER BY total_vacancies DESC, employer_name")
        return result

    def get_all_vacancies(self) -> list:
        """ Метод получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию"""
        result = self._execute_query("SELECT employers.employer_name, vacancy_name, salary, url "
                                     "FROM vacancies "
                                     "JOIN employers USING(employer_id)"
                                     "WHERE salary IS NOT NULL "
                                     "ORDER BY salary DESC, vacancy_name")
        return result

    def get_avg_salary(self) -> list:
        """Метод получает среднюю зарплату по вакансиям"""
        result = self._execute_query("SELECT ROUND(AVG(salary)) as average_salary "
                                     "FROM vacancies")
        return result

    def get_vacancies_with_higher_salary(self) -> list:
        """Метод получает список всех вакансий, у которых зарплата выше средней по всем вакансиям"""
        result = self._execute_query("SELECT vacancy_name, salary "
                                     "FROM vacancies "
                                     "WHERE salary > (SELECT AVG(salary) FROM vacancies) "
                                     "ORDER BY salary DESC, vacancy_name")
        return result

    def get_vacancies_with_keyword(self, word: str) -> list:
        """Метод получает список всех вакансий, в названии которых содержатся переданные в метод слова, например “Python”"""
        result = self._execute_query("SELECT vacancy_name "
                                     "FROM vacancies "
                                     f"WHERE vacancy_name ILIKE '%{word}%'"
                                     "ORDER BY vacancy_name")
        return result