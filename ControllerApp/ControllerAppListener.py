from ControllerAppHandlers import ControllerAppHandlers
from ControllerAppSender import ControllerAppSender
from ControllerAppTaskScheduler import ControllerAppTaskScheduler
from ControllerAppConstants import CONTROLLER_QUEUE, SUPPRESS_LOG_LISTENER
from pika import BlockingConnection, ConnectionParameters
from threading import Thread
from json import loads
from ast import literal_eval
import ControllerAppQueue


class ControllerAppListener(object):
    def __init__(self, 
                 queue, 
                 sender=None, 
                 task_scheduler=None, 
                 node_controller=None, 
                 queue_name=CONTROLLER_QUEUE, 
                 message_handler_mapper=None,
                 amazon=None):
        self.queue = queue
        self.sender = sender
        self.task_scheduler = task_scheduler
        self.node_controller = node_controller
        self.amazon = amazon
        self.set_message_handler_mapper(self.get_default_message_handler_mapper() if message_handler_mapper is None else message_handler_mapper)
        self.queue.get_channel().basic_consume(
            queue=queue_name,
            on_message_callback=self.callback_method,
            auto_ack=True
        )

    def callback_method(self, ch, method, properties, body):
        try:
            message = self.binary_to_dict(body)
            if not (('message' in message and 'args' in message) and (isinstance(message['message'], str) and isinstance(message['args'], dict))):
                raise Exception()
            if not message['message'] in SUPPRESS_LOG_LISTENER:
                print(f'Message being handled. {message}')
            self.handle_message(message)
        except Exception as e:
            print(f'Cannot handle message. {message} {e}')
            raise e

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
        handlers = ControllerAppHandlers(self.sender, self.queue, self.task_scheduler, self, self.node_controller, self.amazon)
        return {
            'calc_route': handlers.calc_route,
            'kill': handlers.kill,
            'healthcheck': handlers.healthcheck,
            'ping_healthcheck': handlers.ping_healthcheck,
        }
