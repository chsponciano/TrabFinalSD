from pika import BlockingConnection, ConnectionParameters
from ControllerAppConstants import CONTROLLER_QUEUE, SERVER_IP


class ControllerAppQueue(object):
    def __init__(self, queue_name=CONTROLLER_QUEUE):
        self.connection = BlockingConnection(ConnectionParameters(SERVER_IP))
        self.channel = self.connection.channel()
        self.queue_name = queue_name
        self.channel.queue_declare(queue=self.queue_name)

    def get_channel(self):
        return self.channel

    def self_delete(self):
        self.channel.queue_delete(queue=self.queue_name)

    def close_connection(self):
        self.connection.close()

    def get_queue_name(self):
        return self.queue_name
