from math import inf as INFINITY
from NodeDAO import NodeDAO

class ServerAppMapper(object):
    def __init__(self, queue):
        # self.connected_queues = set()
        self.queue_mapper = dict()
        self.dao = NodeDAO()
        self.queue = queue

    # def connect_to(self, queue: str):
    #     if self.is_connected_to(queue):
    #         raise Exception()
    #     else:
    #         self.connected_queues.add(queue)
    #         self.queue_mapper[queue] = {'dist': INFINITY}

    def is_connected_to(self, queue: str):
        return self.dao.exists_connection_by_node_id_1_and_node_id_2(self.dao.find_id_by_node_name(self.queue.get_queue_name()), self.dao.find_id_by_node_name(queue))

    def get_connections(self):
        return self.dao.find_all_connections(self.dao.find_id_by_node_name(self.queue.get_queue_name()))

    def get_queue_mapper(self):
        return self.queue_mapper

    def add_to_queue_mapper(self, node: str,  properties: dict):
        self.queue_mapper[node] = properties

    # def remove_connection(self, node: str):
    #     del self.queue_mapper[node]
    #     if node in self.connected_queues:
    #         self.connected_queues.remove(node)

    def find_any_not_in(self, connections):
        for connection in self.get_connections():
            if not connection in connections:
                return connection
        return None
