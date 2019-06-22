from ControllerAppConstants import SERVER_IP, DB_USER, DB_PASS, DB_NAME
from colorama import Fore, Style
import MySQLdb


class NodeDAO(object):
    def __init__(self):
        self.db = MySQLdb.connect(SERVER_IP, DB_USER, DB_PASS, DB_NAME)
        self.cursor = self.db.cursor()

    def exists_by_node_name(self, node_name) -> bool:
        self.cursor.execute(f'SELECT id FROM nodes WHERE node_name = "{node_name}"')
        return self.cursor.rowcount != 0
    
    def find_all_node_name_and_processing_time_and_connections(self) -> list:
        sql = f'SELECT id, node_name, processing_time FROM nodes'
        self.cursor.execute(sql)
        results = list(self.cursor.fetchall())
        final_results = []
        for result in results:
            self.cursor.execute(f'SELECT nodes.node_name FROM nodes INNER JOIN node_connections ON nodes.id = node_connections.node_id_1 WHERE node_connections.node_id_2 = {result[0]}')
            node_connections_result = list(self.cursor.fetchall())
            node_connections_final_result = []
            for node_connection in node_connections_result:
                node_connections_final_result.append(node_connection[0])
            final_results.append({
                'node_name': result[1],
                'processing_time': result[2],
                'connections': node_connections_final_result
            })
        return final_results

    def create(self, node_name: str, processing_time: int, pinged_back: bool) -> None:
        self._execute_in_transaction(f'INSERT INTO nodes VALUES (null, "{node_name}", {processing_time}, {pinged_back})')

    def find_id_by_node_name(self, node_name):
        sql = f'SELECT id FROM nodes WHERE node_name = "{node_name}"'
        self.cursor.execute(sql)
        result = list(self.cursor.fetchall())
        assert len(result) is 1
        return result[0][0]

    def create_connection_between(self, node_id_1: int, node_id_2: int):
        sql = f'SELECT * FROM node_connections WHERE node_id_1 = {node_id_1} AND node_id_2 = {node_id_2}'
        self.cursor.execute(sql)
        assert len(list(self.cursor.fetchall())) is 0
        self._execute_in_transaction(f'INSERT INTO node_connections VALUES ({node_id_1}, {node_id_2})')

    def find_all_node_name_and_processing_time_and_connections_by_pinged_back(self, value):
        sql = f'SELECT id, node_name, processing_time FROM nodes WHERE pinged_back = {value}'
        self.cursor.execute(sql)
        results = list(self.cursor.fetchall())
        final_results = []
        for result in results:
            self.cursor.execute(f'SELECT nodes.node_name FROM nodes INNER JOIN node_connections ON nodes.id = node_connections.node_id_1 WHERE node_connections.node_id_2 = {result[0]}')
            node_connections_result = list(self.cursor.fetchall())
            node_connections_final_result = []
            for node_connection in node_connections_result:
                node_connections_final_result.append(node_connection[0])
            final_results.append({
                'node_name': result[1],
                'processing_time': result[2],
                'connections': node_connections_final_result
            })
        return final_results

    def get_all_node_ids(self):
        sql = f'SELECT id FROM nodes'
        self.cursor.execute(sql)
        results = list(self.cursor.fetchall())
        final_results = []
        for result in results:
            final_results.append(result[0])
        return final_results

    def set_pinged_back(self, node_id, value):
        self._execute_in_transaction(f'UPDATE nodes SET pinged_back = {value} WHERE id = {node_id}')

    def find_all_node_name(self):
        sql = f'SELECT node_name FROM nodes'
        self.cursor.execute(sql)
        results = list(self.cursor.fetchall())
        final_results = []
        for result in results:
            final_results.append(result[0])
        return final_results

    def set_pinged_back_by_node_name(self, node_name, value):
        self._execute_in_transaction(f'UPDATE nodes SET pinged_back = {value} WHERE node_name = "{node_name}"')

    def _execute_in_transaction(self, sql: str):
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as e:
            print(f'{Fore.RED}Error in database transaction.\n{e}\n{sql}{Style.RESET_ALL}')
            self.db.rollback()
