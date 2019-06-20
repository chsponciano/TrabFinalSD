class ServerAppMapper(object):
    def __init__(self):
        self.connected_queues = set()
        self.queue_mapper = dict()

    def connect_to(self, queue: str):
        if self.is_connected_to(queue):
            raise Exception()
        else:
            self.connected_queues.add(queue)
            self.queue_mapper[queue] = {'dist': 1}

    def is_connected_to(self, queue: str) -> bool:
        return queue in self.connected_queues

    def get_connections(self):
        return self.connected_queues

    def get_queue_mapper(self):
        return self.queue_mapper

    def add_to_queue_mapper(self, node: str,  properties: dict):
        self.queue_mapper[node] = properties