-- Запрос на создание базы данных(создается по наименованию пользователя)
CREATE DATABASE "NAME DB";

--Запрос на создание таблиц employers и vacancies
CREATE TABLE IF NOT EXISTS employers '
(
    employer_id int PRIMARY KEY,
    employer_name varchar(255) UNIQUE NOT NULL);

CREATE TABLE IF NOT EXISTS vacancies
(
       vacancy_id int PRIMARY KEY,
       vacancy_name varchar(255) NOT NULL,
       employer_id int REFERENCES employers(employer_id) NOT NULL,
       city varchar(255),
       salary int,
       url text,
       date_published timestamp);
--Запрос на добавление данных в таблицы employers и vacancies
INSERT INTO employers(employer_id, employer_name)
VALUES(%s, %s), data

INSERT INTO vacancies (vacancy_id, vacancy_name, employer_id, city, salary, url, date_published)
VALUES(%s, %s, %s, %s, %s, %s, %s) ON CONFLICT (vacancy_id) DO NOTHING, data

--Запрос на получение список всех компаний и количество вакансий у каждой компании
SELECT employer_name, COUNT(*) as total_vacancies
FROM vacancies
LEFT JOIN employers USING(employer_id)
GROUP BY employer_name
ORDER BY total_vacancies DESC, employer_name

--Запрос на получение списка всех вакансий с указанием названия компании,названия вакансии и зарплаты и ссылки на вакансию
SELECT employers.employer_name, vacancy_name, salary, url
FROM vacancies
JOIN employers USING(employer_id)
WHERE salary IS NOT NULL
ORDER BY salary DESC, vacancy_name

--Запрос на получение средней зарплаты по вакансиям
SELECT ROUND(AVG(salary)) as average_salary
FROM vacancies

--Запрос на получение исок всех вакансий, у которых зарплата выше средней по всем вакансиям
SELECT vacancy_name, salary
FROM vacancies
WHERE salary > (SELECT AVG(salary) FROM vacancies)
ORDER BY salary DESC, vacancy_name

--Запрос получения списка  всех вакансий, в названии которых содержатся переданные в метод слова
SELECT vacancy_name
FROM vacancies
WHERE vacancy_name ILIKE '%{word}%'
ORDER BY vacancy_name
