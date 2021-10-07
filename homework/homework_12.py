import argparse
from datetime import datetime
import psycopg2
from flask import Flask, request
"""
Начните писать своё собственное простое web-приложение. Можно использовать фреймворк Flask или
Sanic (если решите писать асинхронное приложение) по вашему вкусу. Реализовать следующие endpoints ("ручки"):


- создание заявки
- изменение заявки


В рамках выполнения задания вам потребуется взаимодействовать с БД Postgresql.
Используйте для этого библиотеку psycopg2 или asyncpg (если решили писать асинхронный код).
"""
""""""


# for Luchanos:
#     curl --location --request POST '127.0.0.1:5000/create_new_order' \
#     --header 'Content-Type: application/json' \
#     --data-raw '{
#         "orderType": "Поточний ремонт",
#         "description": "Заміна патрубка",
#         "serial_no": 5555,
#         "creator_id": 3
#     }'
#
# curl --location --request PUT '127.0.0.1:5000/update_order' \
# --header 'Content-Type: application/json' \
# --data-raw '{
#     "order_id": "1",
#     "description": "Заміна фільтра"
# }'
""""""

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

# Создаю объект application, основным файлом для работы с классом Flask будет являться этот файл.
application = Flask(__name__)

# Этот тестовый клиент, который нужен на этапе разраболтки для тестирования API.
client = application.test_client()


# Будем отслеживать главную страницу
@application.route('/', methods=['GET'])
def index():
    return "Hello, dear client. Yoc can create order or update order with this web-application"


@application.route('/create_new_order', methods=['POST'])
def create_new_order():
    date_of_request = str((datetime.today()).replace(microsecond=0))
    new_order = request.json

    insert_into_orders_table = f"""INSERT INTO orders (
                                    created_dt,
                                    order_type,
                                    description,
                                    status,
                                    serial_no,
                                    creator_id) VALUES (
                                    '{date_of_request}',
                                    '{new_order['orderType']}',
                                    '{new_order['description']}',
                                    'New',
                                    {new_order['serial_no']},
                                    {new_order['creator_id']}
                                    );"""

    with connection_to_database.cursor() as cursor:
        cursor.execute(insert_into_orders_table)
        connection_to_database.commit()

        select_order_id_by_value = f"""SELECT order_id FROM orders WHERE "created_dt" = '{date_of_request}' AND
                                    "order_type" = '{new_order['orderType']}' AND
                                    "description"= '{new_order['description']}' AND
                                    "status" = 'New' AND
                                    "serial_no" = {new_order['serial_no']} AND
                                    "creator_id"= {new_order['creator_id']};"""

        cursor.execute(select_order_id_by_value)
        order_id = cursor.fetchall()
    return f"New order {order_id} was added."


@application.route('/update_order', methods=['PUT'])
def update_order():
    date_of_request = str((datetime.today()).replace(microsecond=0))
    upd_order = request.json
    with connection_to_database.cursor() as cursor:
        for k in upd_order:
            if k == 'order_id':
                update_orders_description = f"""UPDATE orders SET "update_dt" = '{date_of_request}', 
                                                "description" = '{upd_order['description']}', 
                                                "status" = 'New' WHERE 
                                                "order_id" = {upd_order['order_id']};"""
                cursor.execute(update_orders_description)

        connection_to_database.commit()
        return f"The order {upd_order['order_id']} was updated with value: '{upd_order['description']}'."


# Условние если этот файл является основым файлом запуска. Команда run запускает локальный сервер.
# параметр debug = True выводит возможные ошибки в клиент.
if __name__ == '__main__':
    application.run(debug=True)
