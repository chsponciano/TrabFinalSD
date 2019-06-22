from pika import BlockingConnection, ConnectionParameters
from ControllerAppConstants import *


class ControllerAppQueue(object):
    def __init__(self):
        self.connection = BlockingConnection(ConnectionParameters(SERVER_IP))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=CONTROLLER_QUEUE)

    def get_channel(self):
        return self.channel

    def close_connection(self):
        self.connection.close()
