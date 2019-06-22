from dao.NodeDAO import NodeDAO


class NodeController(object):
    def __init__(self):
        self.dao = NodeDAO()

    def has_control_over_nodes(self, *args):
        for node_name in args:
            if not self.dao.exists_by_node_name(node_name):
                return False
        return True

    def get_all_nodes(self):
        return self.dao.find_all_node_name_and_processing_time_and_connections()

    def create_node(self, node_name, processing_time):
        self.dao.create(node_name, processing_time, False)

    def exists(self, node_name):
        return self.dao.exists_by_node_name(node_name)

    def add_connection_to(self, node_name, connection_name):
        id_node = self.dao.find_id_by_node_name(node_name)
        id_connection = self.dao.find_id_by_node_name(connection_name)
        self.dao.create_connection_between(id_node, id_connection)

    def get_down_nodes(self):
        return self.dao.find_all_node_name_and_processing_time_and_connections_by_pinged_back(False)

    def reset_all_pinged_back(self):
        node_ids = self.dao.get_all_node_ids()
        for node_id in node_ids:
            self.dao.set_pinged_back(node_id, False)

    def get_all_node_names(self):
        return self.dao.find_all_node_name()
    
    def set_pinged_back(self, node_name, value):
        self.dao.set_pinged_back_by_node_name(node_name, value)

