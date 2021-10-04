"""
Организовать взаимодействие клиента и сервера:
клиент открывает json-файл (который вы можете создать руками и наполнить) и осуществляет его отправку на сервер.
Сервер принимает данные и сохраняет json-файл в произвольной директории, а также выводит на экран консоли время
принятия json-файла с помощью объекта логгера из библиотеки logging.
"""

import json
import socket
import time
from datetime import datetime

from logging import getLogger
from pathlib import Path

server = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)
server.bind(
    ("127.0.0.1", 10002)
)
server.listen(socket.SOMAXCONN)


def get_project_root() -> Path:
    return Path(__file__).parent


directory_path = get_project_root() / "Download"

logger = getLogger(__name__)
logger.setLevel("DEBUG")

while True:
    user_socket, address = server.accept()
    user_socket.settimeout(60)
    user_socket.send("You have connect".encode("utf-8"))

    logfile = open("logfile_one.txt", "a")
    with user_socket, server, logfile:
        while True:
            data_as_bytes = user_socket.recv(2048)
            data_as_str = data_as_bytes.decode("utf-8")
            data_as_json = json.dumps(json.loads(data_as_str))
            f = open(f'{directory_path}/data_from_client.json', 'a')
            f.write(data_as_json)
            f.close()
            logger.error(f"{datetime.now()}, {data_as_str}")
            time.sleep(1)
            if not data_as_bytes:
                break

