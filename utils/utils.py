import json
import requests
from datetime import datetime, time
import time


def getEmployers():
    """Функция позволяющий положить данные о всех работодателях на рынке в словарь"""
    # Получаем данные о работодателях с HH
    response = requests.get('https://api.hh.ru/employers')
    data = response.content.decode()
    response.close()

    # Складываем данные о работодателе в файл
    count_of_employers = json.loads(data)['found']
    employers = []
    i = 0
    j = int(input('Введите ограничение по id\n'))
    while i < j:
        req = requests.get('https://api.hh.ru/employers/' + str(i + 1))
        data = req.content.decode()
        req.close()
        jsObj = json.loads(data)

        try:
            employers.append({"title": jsObj['name'], "id": jsObj['id']})
            i += 1
            print({jsObj['id']: jsObj['name']})

        except:
            i += 1

        if i % count_of_employers == 0:
            time.sleep(0.2)
    return employers


def insert_employers(PATH: str, data: list):
    """Функция записи данных о работодателях с HH с сохранением в файл """

    with open(PATH, 'w', encoding='UTF-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def read_json(file) -> list:
    """Функция для чтения json-файл"""

    with open(file,'r', encoding='UTF-8') as f:
        data = json.load(f)
    return data

def get_employers(data: list) -> list:
    """Функция получает список кортежей из списка словарей"""

    employers = []
    for item in data:
        employers.append((item['id'], item['title']))
    return employers

def print_info(choice: str, data: list):
    """Функция печатает информацию в зависимости от выбора пользователя"""
    if choice == '3':
        salary = ''
        for item in str(data):
            if item.isdigit():
                salary += item
        return salary

    else:
        count = 1
        for item in data:

            if choice == '1':
                print(f'{count}. {item[0]} - {item[1]} вакансий')
            elif choice == '2':
                print(f'{count}. {item[1]} - {item[0]}({item[3]}), зарплата - {item[2]}')
            elif choice == '4':
                print(f'{count}. {item[0]} - {item[1]} рублей')
            elif choice == '5':
                print(f'{count}. {item[0]}')

            count += 1