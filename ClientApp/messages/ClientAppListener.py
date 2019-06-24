from pika import BlockingConnection, ConnectionParameters
from ClientAppSender import ClientAppSender
from ClientAppConstants import SUPPRESS_LOG_LISTENER, FRONTEND_QUEUE
from threading import Thread
from json import loads
from ast import literal_eval
import ClientAppQueue
import subprocess


class ClientAppListener(object):
    def __init__(self, queue: ClientAppQueue, sender: ClientAppSender, websocket):
        self.queue = queue
        self.websocket = websocket
        self.queue.get_channel().basic_consume(
            queue=FRONTEND_QUEUE,
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

    def handle_message(self, message: dict):
        if message["message"] == "create_node":
            self.exec_comm_docker("docker run -it --network graph-network chsponciano/noderabbit python ServerAppInitialize.py " + message["args"]["node_name"] + " " + message["args"]["processing_time"])
        elif message["message"] == "delete_node":
            self.exec_comm_docker("docker rm -f " + message["args"]["node_name"])

        self.websocket.add_message(message)

    def binary_to_dict(self, binary_json) -> dict:
        return literal_eval(binary_json.decode('utf-8'))

    def start_listening(self):
        print(f'Começou a consumir a fila {FRONTEND_QUEUE}.')
        self.queue.get_channel().start_consuming()

    def start_listening_async(self):
        thread = Thread(target=self.start_listening)
        thread.start()

    def stop_listening(self):
        self.queue.get_channel().stop_consuming()

    def exec_comm_docker(self, command):
        with open("output.log", "a") as output:
            subprocess.call(command, shell=True, stdout=output, stderr=output)
