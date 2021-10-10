import asyncio
import json


class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    async def handle_echo(self, reader, writer):

        data = await reader.read(2048) # считывает данные из сокета. writer - для записи в сокет
        message = data.decode("utf-8")

        # addr = writer.get_extra_info('peername')
        print(message)
        # print('received %r from %r' % (message, addr))

        writer.write(f"echo server - {message}".encode("utf-8"))
        writer.close()

    def run_server(self):
        """Запускает сервер в вечном цикле"""
        loop = asyncio.get_event_loop()
        coro = asyncio.start_server(client_connected_cb=self.handle_echo, host=self.host, port=self.port,
                                    loop=loop)  # передали параметры
        loop.run_until_complete(coro)

        try:
            loop.run_forever()
        except KeyboardInterrupt:
            print("Server stopped by keyboard")
            loop.close()


# serv = Server(host='127.0.0.1', port=5000)
# serv.run_server()
