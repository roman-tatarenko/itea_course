"""
Давайте создадим ещё одну интеграцию для поступления заявок в наш сервис техподдержки -
на этот раз с использованием RabbitMQ. Необходимо:


- реализовать sender (отправитель) для использования на стороне клиента.
Он должен отправлять в произвольную очередь сообщения с информацией о создаваемой заявке.
- реализовать consumer (потребитель) для вычитывания сообщений из очереди и создания соответствующей
записи об этом в базе данных.


Рекомендую использовать библиотеку pika или aio-pika (если хотите реализовать это асинхронно)
"""
import json

from pika import PlainCredentials, BlockingConnection, ConnectionParameters

# Это sender
connection = BlockingConnection(ConnectionParameters(
    host='127.0.0.1',
    credentials=PlainCredentials(username='rmquser', password='rmqpass')
))

# Это канал для передачи данных
channel = connection.channel()

# Это сообщение в очередь
new_order = {
    "orderType": "Поточний ремонт",
    "description": "Заміна патрубка",
    "serial_no": 6666,
    "creator_id": 1
}
for num in range(4):
    channel.basic_publish(
        exchange='',
        routing_key='test_queue',
        body=f'{json.dumps(new_order)}'.encode()
    )
    print(f"Message {num} was sent")
connection.close()
