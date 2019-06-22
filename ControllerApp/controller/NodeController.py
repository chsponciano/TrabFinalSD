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
        return self.dao.find_all_node_name_and_processing_time()

    def create_node(self, node_name, processing_time):
        self.dao.create(node_name, processing_time, False)

    def exists(self, node_name):
        return self.dao.exists_by_node_name(node_name)
