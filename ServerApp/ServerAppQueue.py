from pika import BlockingConnection, ConnectionParameters
from ServerAppConstants import *


class ServerAppQueue(object):
    def __init__(self, queue_name='fila-teste'):
        self.queue_name = queue_name
        self.connection = BlockingConnection(ConnectionParameters(SERVER_IP))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.get_queue_name())

    def get_queue_name(self):
        return self.queue_name

    def get_channel(self):
        return self.channel

    def close_connection(self):
        self.connection.close()
