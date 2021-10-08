import argparse
import json
from datetime import datetime

import psycopg2
from pika import BlockingConnection, ConnectionParameters, PlainCredentials

# Это consumer
connection = BlockingConnection(ConnectionParameters(
    host='127.0.0.1',
    credentials=PlainCredentials(username='rmquser', password='rmqpass')
))

# Это канал для передачи данных
channel = connection.channel()

# парсим аргументы с командной строки для БД
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


def create_order(ch, method, properties, body):
    new_order = json.loads(body.decode())
    date_of_request = str((datetime.today()).replace(microsecond=0))
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

    print(f" Новая заявка! - {new_order}")
    ch.basic_ack(delivery_tag=method.delivery_tag)


# создаём базовый консумер (консумер = потребитель сообщений)
channel.basic_consume(on_message_callback=create_order,
                      queue='test_queue',
                      auto_ack=False,
                      consumer_tag="Mr.Rabbit")

channel.start_consuming()
