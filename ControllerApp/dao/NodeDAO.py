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
    
    def find_all_node_name_and_processing_time(self) -> list:
        sql = f'SELECT node_name, processing_time FROM nodes'
        self.cursor.execute(sql)
        results = list(self.cursor.fetchall())
        final_results = []
        for result in results:
            final_results.append({
                'node_name': result[0],
                'processing_time': result[1]
            })
        return final_results # [{'node_name': '', 'processing_time': ''}]

    def create(self, node_name: str, processing_time: int, pinged_back: bool) -> None:
        self._execute_in_transaction(f'INSERT INTO nodes VALUES (null, "{node_name}", {processing_time}, {pinged_back})')

    def _execute_in_transaction(self, sql: str):
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as e:
            print(f'{Fore.RED}Error in database transaction.\n{e}\n{sql}{Style.RESET_ALL}')
            self.db.rollback()
