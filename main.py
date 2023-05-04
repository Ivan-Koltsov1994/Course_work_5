# Добавляем требуемые импорты
from utils.config import config
from utils.utils import getEmployers, insert_employers, read_json, get_employers, print_info
from classes.dbManager import DBManager
from classes.hh import HH

# Требуемые ссылки и массивы данных
PATH_TO_EMPLOYERS_BASE = 'data/employers_base.json'
employers = []


def main():
    # Подключаемся к postgreSQL и создаем новую базу данных
    params = config()

    print('Подключаемся к базе данных postges\n ..........................')
    dbname = input("Введите имя базы данных\n")  # Вводим имя новой базы данных
    db = DBManager(f'{dbname}', params)

    # Создаем новую базу данных
    print('Идет создание базы данных\n ..........................')
    db.create_database()
    print('База данных с таблицами employers и vacancies создана\n ..........................')

    # Запрашиваем у пользователя данные о том, скачивал ли он до этого данные о вакансиях
    user_input_employers = input(
        f"Вы сохраняли данные о работодателях ранее в файле {PATH_TO_EMPLOYERS_BASE}\n").lower()

    if user_input_employers == 'да' or user_input_employers == 'уes':
        employers_base = read_json(PATH_TO_EMPLOYERS_BASE)
        print(f"Данные о работодателях хранятся в файле{PATH_TO_EMPLOYERS_BASE}")
    else:
        data_employers = getEmployers()
        insert_employers(PATH_TO_EMPLOYERS_BASE, data_employers)
        employers_base = read_json(PATH_TO_EMPLOYERS_BASE)
        print(f"Данные о работодателях хранятся в файле: {PATH_TO_EMPLOYERS_BASE}")
        print(f"Список всех работодателей можно посмотреть в файле: {PATH_TO_EMPLOYERS_BASE}")

    # Выбираем нужные вакансии из сохраненной базы в JSON-файле
    while True:
        keyword_count_employers = int(input('Введите требуемое количество работодателей:\n'))
        count = 0
        for i in range(keyword_count_employers):
            keyword_employers = input('Введите имя компании:\n')
            for i in employers_base:
                if keyword_employers == i["title"]:
                    employers.append(i)
                    count += 1
        if count == keyword_count_employers:
            break

    # Добавляем данные в тааблицу employers
    print('Вы выбрали работодателей\nДобавляем данные работодателей в таблицу employers')
    db.insert_data('employers', get_employers(employers))
    print('Данные о работодателях  добавлены в таблицу employers')

    # Добавляем данные о вакансиях на основании таблицы employers
    print('Добавляем данные о вакансиях\n................................')

    for i in range(len(employers)):
        hh = HH(employers[i]['id']).get_vacancies()
        db.insert_data('vacancies', hh)
    print('Вакансии добавлены в БД\n................................')

    # Взаимодействие пользователя с базой данных
    while True:

        print(f'Вашему вниманию предлагаются следующие варианты поиска вакансий:\n\
            1 - получить список всех компаний и количество вакансий у каждой компании\n\
            2 - получить список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на '
              f'вакансию\n\
            3 - получить среднюю зарплату по вакансиям\n\
            4 - получить список всех вакансий, у которых зарплата выше средней по всем вакансиям\n\
            5 - получить список всех вакансий, в названии которых содержатся переданное в метод слово\n\
            stop - закончить работу\n')

        user_input = input("Пожалуйста, выберете нужный вариант:\n")

        if user_input == '1':
            print('Компании от большего количества вакансий к наименьшему')
            print_info(choice=user_input, data=db.get_companies_and_vacancies_count())

        elif user_input == '2':
            all_vacancies = db.get_all_vacancies()
            print(f'Всего вакансий, где указана зарплата - {len(all_vacancies)}.\n'
                  'Вакансии отсортированы по зарплате от большей к меньшей')
            print_info(choice=user_input, data=all_vacancies)

        elif user_input == '3':
            print(f'Средняя зарплата по всем вакансиям - {print_info(choice=user_input, data=db.get_avg_salary())} '
                  f'рублей')

        elif user_input == '4':
            all_vacancies = db.get_vacancies_with_higher_salary()
            print(f'Всего вакансий, где зарплата выше средней по всем вакансиям  в БД - {len(all_vacancies)}')
            print_info(choice=user_input, data=all_vacancies)

        elif user_input == '5':
            keyword = input('Введите слово, которое будем искать в названии вакансии\n')
            all_vacancies = db.get_vacancies_with_keyword(keyword)
            print(f'Всего вакансий, содержащих "{keyword}" - {len(all_vacancies)}')
            print_info(choice=user_input, data=all_vacancies)

        elif user_input.lower() == 'stop':
            print('Программа завершает работу')
            break

        else:
            print("Такого варианта нет, попробуйте еще раз")
            continue

        print('Показать еще меню? ДА/НЕТ')
        keyword_user = input().upper()
        if keyword_user == 'YES' or keyword_user == 'ДА':
            continue
        else:
            print('Спасибо,что пользуетесь нашим приложением!\nХорошего дня!')
            break

if __name__ == '__main__':
    main()