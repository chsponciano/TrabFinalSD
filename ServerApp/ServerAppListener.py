from pika import BlockingConnection, ConnectionParameters
from ServerAppHandlers import ServerAppHandlers
from ServerAppSender import ServerAppSender
from ServerAppMapper import ServerAppMapper
from threading import Thread
from json import loads
from ast import literal_eval
import ServerAppQueue


class ServerAppListener(object):
    def __init__(self, queue: ServerAppQueue, sender: ServerAppSender, mapper: ServerAppMapper):
        self.queue = queue
        self.handlers = ServerAppHandlers(sender, self.queue, mapper)
        self.queue_name = self.queue.get_queue_name()
        self.set_message_handler_mapper(
            self.get_default_message_handler_mapper())
        self.queue.get_channel().basic_consume(
            queue=self.queue_name,
            on_message_callback=self.callback_method,
            auto_ack=True
        )

    def callback_method(self, ch, method, properties, body):
        try:
            message = self.binary_to_dict(body)
            if not (('message' in message and 'args' in message) and (isinstance(message['message'], str) and isinstance(message['args'], dict))):
                raise Exception()
            print(f'Message being handled. {message}')
            self.handle_message(message)
        except Exception as e:
            print(f'Cannot handle message. {message} {e}')

    def handle_message(self, message: dict):
        mapper = self.get_message_handler_mapper()
        if message['message'] in mapper:
            mapper[message['message']](message['args'])
        else:
            print(f'No implementation for {message} found!')

    def binary_to_dict(self, binary_json) -> dict:
        return literal_eval(binary_json.decode('utf-8'))

    def start_listening(self):
        self.queue.get_channel().start_consuming()

    def start_listening_async(self):
        thread = Thread(target=self.start_listening)
        thread.start()

    def stop_listening(self):
        self.queue.get_channel().stop_consuming()

    def set_message_handler_mapper(self, message_handler_mapper):
        self.message_handler_mapper = message_handler_mapper

    def get_message_handler_mapper(self):
        return self.message_handler_mapper

    def get_default_message_handler_mapper(self):
        return {
            'connect_to': self.handlers.connect_to,
            'ping_everyone': self.handlers.ping_everyone,
            'ping': self.handlers.ping,
            'dijkstra': self.handlers.dijkstra,
            'start_dijkstra': self.handlers.start_dijkstra,
            'dijkstra_done': self.handlers.dijkstra_done
        }
