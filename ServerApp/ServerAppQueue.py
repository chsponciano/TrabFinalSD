from pika import BlockingConnection, ConnectionParameters
from ServerAppConstants import *


class ServerAppQueue(object):
    def __init__(self, queue_name='fila-teste', processing_time=1):
        self.queue_name = queue_name
        self.processing_time = int(processing_time)
        self.connection = BlockingConnection(ConnectionParameters(SERVER_IP))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.get_queue_name())

    def get_queue_name(self):
        return self.queue_name

    def get_channel(self):
        return self.channel

    def get_processing_time(self):
        return self.processing_time

    def close_connection(self):
        self.connection.close()
