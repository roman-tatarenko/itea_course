import json
import socket
from pathlib import Path

client = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)
client.connect(
    ("127.0.0.1", 6000)
)

while True:
    data = client.recv(2048)
    print(data.decode("utf-8"))
    data_for_sending = {4: False}
    client.send(str(data_for_sending).encode("utf-8"))
