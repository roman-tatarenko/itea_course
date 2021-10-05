"""
Создать таблицу пользователи (Users или использовать любую подобную таблицу из прошлого ДЗ) в которой будут
колонки имя (username), активность подписки (is_subscribed).
Написать простой сервер (синхронный или асинхронный), который будет принимать сообщение о том, что пользователя
с определённым id надо подписать или отписать от уведомлений и вносить соответствующие изменения в БД
"""
import argparse
import socket
import time
from datetime import datetime

from logging import getLogger


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

server = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)
server.bind(
    ("127.0.0.1", 6000)
)
server.listen(socket.SOMAXCONN)

logger = getLogger(__name__)
logger.setLevel("DEBUG")

while True:
    user_socket, address = server.accept()
    user_socket.settimeout(60)
    user_socket.send("You have connect".encode("utf-8"))

    logfile = open("logfile_one.txt", "a")
    with user_socket, server, logfile:
        while True:
            data_from_client = user_socket.recv(1024).decode("utf-8")
            data_as_list = data_from_client.replace('{', '').replace('}', '').replace(':', '').split()
            data_from_client_user_id = int(data_as_list[0])
            data_from_client_subscribe = bool(data_as_list[1])
            logger.error(f"{datetime.now()}, {data_as_list}")
            time.sleep(1)
            if not data_from_client:
                break

            update_table = f"""UPDATE Users SET "is_subscribed"={data_from_client_subscribe} WHERE 
            "user_id"='{data_from_client_user_id}';"""
            with connection_to_database.cursor() as cursor:
                cursor.execute(update_table)
                connection_to_database.commit()

