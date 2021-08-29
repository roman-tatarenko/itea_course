"""
Создать тестовый набор данных по каждой из таблиц в модуле python (лучше всего использовать список списков или
список кортежей). Далее написать скрипт, который будет осуществлять подключение к существующей БД и последовательно
запускать сначала скрипты на создание таблиц из прошлого ДЗ: departments, employees, orders, а затем загружал туда
данные.

Написать следующие запросы:
- запрос для получения заявок в определённом статусе (можно выбрать любой) за конкретный день, созданных
конкретным сотрудником;
- запрос, возвращающий список сотрудников и департаментов, в которых они работают;
- запрос, позволяющий получить количество заявок в определенном статусе (можно выбрать любой) по дням;
- запрос, который возвращает таблицу с двумя колонками: id заявок и ФИО сотрудников, которые их создали.
"""
import argparse
import random
from datetime import datetime
from pprint import pprint

import psycopg2

departments_value = [
    'Technical department',
    'Guarantee and capital shop repairs',
    'Storage house'
]

employees_value = [
    ('Ivan Petrenko', 'Master inspector', 1),
    ('Alexey Petrenko', 'Master inspector', 1),
    ('Kira Gaponenko', 'Master inspector', 1),
    ('Illya Petrovichev', 'Engineer', 2),
    ('Mykola Gafronoff', 'Engineer', 2),
    ('Petro Simonoff', 'Engineer', 2),
    ('Mykola Hanover', 'Storekeeper', 3),
    ('Alexander Sidorenko', 'Storekeeper', 3),
    ('Andriy Kramarenko', 'Storekeeper', 3),
]


order_value = [
    (str((datetime.today()).replace(microsecond=0)),
     'ТО', 'Заміна масла', 'Done', int(random.randint(1, 100)), 3),
    (str((datetime.today()).replace(microsecond=0)), 'ТО', 'Заміна масла', 'In progress',
     int(random.randint(1, 100)), 1),
    (str((datetime.today()).replace(microsecond=0)), 'ТО', 'Заміна масла', 'In progress',
     int(random.randint(1, 100)), 2),
    (str((datetime.today()).replace(microsecond=0)), 'Поточний ремонт', 'Ремонт рульової рейки',
     'In progress', int(random.randint(1, 100)), 3)
]

parser = argparse.ArgumentParser()
parser.add_argument("--postgres_username", required=True, type=str)
parser.add_argument("--postgres_password", required=True, type=str)
parser.add_argument("--postgres_host", required=True, type=str)
parser.add_argument("--postgres_port", required=True, type=str)
parser.add_argument("--postgres_database", required=True, type=str)
args = parser.parse_args()

DB_URL = f"postgresql://{args.postgres_username}:{args.postgres_password}@{args.postgres_host}:{args.postgres_port}" \
         f"/{args.postgres_database}"

connection_to_database = psycopg2.connect(DB_URL)

create_department_table = """CREATE TABLE departments (
                            department_id SERIAL primary key,
                            department_name text not NULL);"""

insert_into_department_table = "INSERT INTO departments (department_name) VALUES ('{}');"

with connection_to_database.cursor() as cursor:
    cursor.execute(create_department_table)
    for row in departments_value:
        cursor.execute(insert_into_department_table.format(row))
        connection_to_database.commit()


create_employees_table = """CREATE TABLE employees (
                            employee_id SERIAL primary KEY,
                            fio text not NULL,
                            "position" TEXT,
                            department_id INT not NULL,
                            foreign key (department_id) references departments (department_id));"""

insert_into_employees_table = """INSERT INTO employees (
                                fio,
                                position ,
                                department_id) VALUES {};"""

with connection_to_database.cursor() as cursor:
    cursor.execute(create_employees_table)
    for row in employees_value:
        cursor.execute(insert_into_employees_table.format(row))
        connection_to_database.commit()


create_orders_table = """CREATE TABLE orders
                        (order_id SERIAL primary key,
                        created_dt DATE not NULL,
                        update_dt DATE,
                        order_type text not Null,
                        description TEXT,
                        status text not NUll,
                        serial_no INT not NUll,
                        creator_id INT not NUll,
                        foreign key (creator_id) references employees (employee_id));"""

insert_into_orders_table = """INSERT INTO orders (
                                created_dt,
                                order_type,
                                description,
                                status,
                                serial_no,
                                creator_id) VALUES {};"""

with connection_to_database.cursor() as cursor:
    cursor.execute(create_orders_table)
    for row in order_value:
        cursor.execute(insert_into_orders_table.format(row))
        connection_to_database.commit()

select_orders_by_status = """SELECT * FROM orders WHERE status = 'Done' and
                            created_dt='2021-08-29' and creator_id=3;"""
with connection_to_database.cursor() as cursor:
    cursor.execute(select_orders_by_status)
    pprint(cursor.fetchall())

select_employees_and_departments = """SELECT fio, department_name FROM employees INNER JOIN departments
                                        ON employees.department_id= departments.department_id;"""
with connection_to_database.cursor() as cursor:
    cursor.execute(select_employees_and_departments)
    print(cursor.fetchall())

select_count_of_orders_by_status_by_date = """SELECT count(status) FROM orders WHERE
                                                created_dt='2021-08-29' AND status='In progress';"""
with connection_to_database.cursor() as cursor:
    cursor.execute(select_count_of_orders_by_status_by_date)
    print(cursor.fetchall())

select_order_id_and_fio = """SELECT order_id, fio FROM orders INNER JOIN employees ON 
                                orders.creator_id = employees.employee_id;"""
with connection_to_database.cursor() as cursor:
    cursor.execute(select_order_id_and_fio)
    print(cursor.fetchall())
