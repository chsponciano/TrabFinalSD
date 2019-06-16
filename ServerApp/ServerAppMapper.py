class ServerAppMapper(object):
    def __init__(self):
        self.connected_queues = set()

    def connect_to(self, queue: str):
        if self.is_connected_to(queue):
            raise Exception()
        else:
            self.connected_queues.add(queue)

    def is_connected_to(self, queue: str) -> bool:
        return queue in self.connected_queues

    def get_connections(self):
        return self.connected_queues
