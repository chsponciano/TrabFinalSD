from pika import BlockingConnection, ConnectionParameters
from ClientAppConstants import FRONTEND_QUEUE, SERVER_IP


class ClientAppQueue(object):
    def __init__(self):
        self.connection = BlockingConnection(ConnectionParameters(SERVER_IP))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=FRONTEND_QUEUE)

    def get_channel(self):
        return self.channel

    def close_connection(self):
        self.connection.close()
