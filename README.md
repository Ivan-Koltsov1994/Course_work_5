# Course_work_5

Программа получает данные о компаниях и вакансиях с сайта hh.ru, создает таблицы в БД PostgreSQL и загружает полученные данные в созданные таблицы, делает анализ работодателей.

Пользователь сам делает выбор количества и наименования компании, вакансии которых программа будет загружать в БД. Ограничение по id компании в hh пользователь вводит вручную.

Структура репозитория:

main.py - файл для запуска программы
classes - директория классов: hh.py - класс для работы с сайтом hh.ru db_Manager.py - класс для работы с базой данных
utils - директория функций: 
-utils.py - функции для работы программы 
-config.py - функция для получения словаря с данными для подключения к базе данных
tests - директория тестов
data - директория файлов для работы с программой
pyproject.toml - список необходимых пакетов для работы с программой


Перед началом работы программы необходимо:

установить виртуальное окружение
установить пакеты из файла pyproject.toml
создать конфигурационный файл database.ini для подключения к базе данных Шаблон для создания конфигурации: 
[postgresql] 
host=localhost 
user=postgres 
password=1111 
port=5432


Описание работы программы:

Программа собирает данные о вакансиях от пользователя
Создает базу данных и таблицы
Записывает полученные данные в созданные таблицы
Выводит предложения для пользователя
