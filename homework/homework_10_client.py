import socket
from pathlib import Path


def get_project_root() -> Path:
    return Path(__file__).parent


some_file = get_project_root() / "some.json"

client = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)
client.connect(
    ("127.0.0.1", 10002)
)

with open(some_file, "rb") as f:
    data_for_sending = f.read(2048)
while True:
    data = client.recv(2048)
    print(data.decode("utf-8"))

    client.send(data_for_sending)
