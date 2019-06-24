import asyncio
import websockets
import json
from ClientAppInitialize import ClientAppInitialize
from ClientAppConstants import CONTROLLER_QUEUE
from colorama import Style, Fore
from queue import Queue
from time import sleep
from threading import Thread


class ClientAppWebSocket:

    def __init__(self):
        self.client_app = ClientAppInitialize(self)
        self.websocket_sv = None
        self.users = set()
        self.queue_message = Queue()
        self.server = websockets.serve(self.contorller_message, 'localhost', 8765)
        asyncio.get_event_loop().run_until_complete(self.server)
        asyncio.get_event_loop().run_forever()

    def register(self, websockets):
        self.users.add(websockets)

    def add_message(self, message):
        self.queue_message.put(message)

    async def contorller_message(self, websocket, path):
        self.register(websocket)
        self.websocket_sv = websocket
        while True:
            message = json.loads(await self.websocket_sv.recv())
            self.client_app.sender.send_message_to(to=CONTROLLER_QUEUE, message=message)
            aux = False
            while not aux:
                while not self.queue_message.empty():
                    await websocket.send(str(self.queue_message.get()))
                    aux = True
                sleep(1)
                
c = ClientAppWebSocket()