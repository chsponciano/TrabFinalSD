from ServerAppConstants import SERVER_IP, DB_USER, DB_PASS, DB_NAME, SUPPRESS_SQL, DB_HOST
from colorama import Fore, Style
from datetime import datetime
import MySQLdb


class NodeDAO(object):
    def __init__(self):
        self.db = MySQLdb.connect(DB_HOST, DB_USER, DB_PASS, DB_NAME)
        self.cursor = self.db.cursor()

    def exists_by_node_name(self, node_name):
        self.cursor.execute(f'SELECT id FROM nodes WHERE node_name = "{node_name}"')
        return self.cursor.rowcount != 0
    
    def find_all_node_name_and_processing_time_and_connections(self):
        sql = f'SELECT id, node_name, processing_time FROM nodes'
        self._log(sql)
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

    def create(self, node_name, processing_time, pinged_back):
        self._execute_in_transaction(f'INSERT INTO nodes VALUES (null, "{node_name}", {processing_time}, {pinged_back})')

    def find_id_by_node_name(self, node_name):
        sql = f'SELECT id FROM nodes WHERE node_name = "{node_name}"'
        self._log(sql)
        self.cursor.execute(sql)
        result = list(self.cursor.fetchall())
        assert len(result) is 1
        return result[0][0]

    def create_connection_between(self, node_id_1, node_id_2):
        sql = f'SELECT * FROM node_connections WHERE node_id_1 = {node_id_1} AND node_id_2 = {node_id_2}'
        self._log(sql)
        self.cursor.execute(sql)
        assert len(list(self.cursor.fetchall())) is 0
        self._execute_in_transaction(f'INSERT INTO node_connections VALUES ({node_id_1}, {node_id_2})')

    def find_all_node_name_and_processing_time_and_connections_by_pinged_back(self, value):
        sql = f'SELECT id, node_name, processing_time FROM nodes WHERE pinged_back = {value}'
        self._log(sql)
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

    def find_all_node_ids(self):
        sql = f'SELECT id FROM nodes'
        self._log(sql)
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
        self._log(sql)
        self.cursor.execute(sql)
        results = list(self.cursor.fetchall())
        final_results = []
        for result in results:
            final_results.append(result[0])
        return final_results

    def set_pinged_back_by_node_name(self, node_name, value):
        self._execute_in_transaction(f'UPDATE nodes SET pinged_back = {value} WHERE node_name = "{node_name}"')

    def delete_connection(self, node_id_1, node_id_2):
        self._execute_in_transaction(f'DELETE FROM node_connections WHERE node_id_1 = {node_id_1} and node_id_2 = {node_id_2}')

    def find_all_connections(self, node_id):
        sql = f'SELECT nodes.node_name FROM nodes INNER JOIN node_connections ON nodes.id = node_connections.node_id_1 WHERE node_connections.node_id_2 = {node_id}'
        self._log(sql)
        self.cursor.execute(sql)
        result = list(self.cursor.fetchall())
        final_result = []
        for node_connection in result:
            final_result.append(node_connection[0])
        return final_result
    
    def delete_by_node_name(self, node_name):
        self._execute_in_transaction(f'DELETE FROM nodes WHERE node_name = "{node_name}"')

    def exists_connection_by_node_id_1_and_node_id_2(self, node_id_1, node_id_2):
        sql = f'SELECT * FROM node_connections WHERE node_id_1 = {node_id_1} AND node_id_2 = {node_id_2}'
        self._log(sql)
        self.cursor.execute(sql)
        result = list(self.cursor.fetchall())
        return len(result) > 0

    def _execute_in_transaction(self, sql):
        try:
            self._log(sql)
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as e:
            print(f'{Fore.RED}Error in database transaction.\n{e}\n{sql}{Style.RESET_ALL}')
            self.db.rollback()

    def _log(self, sql):
        if not SUPPRESS_SQL:
            print(f'{datetime.now()} - {sql}')
