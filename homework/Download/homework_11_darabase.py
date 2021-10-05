"""
Создать таблицу пользователи (Users или использовать любую подобную таблицу из прошлого ДЗ) в которой будут
колонки имя (username), активность подписки (is_subscribed).
Написать простой сервер (синхронный или асинхронный), который будет принимать сообщение о том, что пользователя
с определённым id надо подписать или отписать от уведомлений и вносить соответствующие изменения в БД
"""

import argparse

import psycopg2


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

create_users_table = """CREATE TABLE Users (
                            user_id SERIAL primary key,
                            username text not NULL,
                            is_subscribed boolean not NULL);"""

users_value = [
    ('Sobi', True),
    ('Tobi', False),
    ('Bobi', False),
    ('Robi', False),
]

insert_into_users_table = "INSERT INTO Users (username, is_subscribed) VALUES {};"

with connection_to_database.cursor() as cursor:
    cursor.execute(create_users_table)
    for row in users_value:
        cursor.execute(insert_into_users_table.format(row))
        connection_to_database.commit()