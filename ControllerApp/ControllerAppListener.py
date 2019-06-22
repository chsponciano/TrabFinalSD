from ControllerAppHandlers import ControllerAppHandlers
from ControllerAppSender import ControllerAppSender
from ControllerAppConstants import CONTROLLER_QUEUE
from pika import BlockingConnection, ConnectionParameters
from threading import Thread
from json import loads
from ast import literal_eval
import ControllerAppQueue


class ControllerAppListener(object):
    def __init__(self, queue: ControllerAppQueue, sender: ControllerAppSender):
        self.queue = queue
        self.handlers = ControllerAppHandlers(sender, self.queue)
        self.set_message_handler_mapper(self.get_default_message_handler_mapper())
        self.queue.get_channel().basic_consume(
            queue=CONTROLLER_QUEUE,
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
            'get_all_nodes': self.handlers.get_all_nodes,
            'calc_route': self.handlers.calc_route,
            'create_node': self.handlers.create_node,
            'connect_nodes': self.handlers.connect_nodes
        }
