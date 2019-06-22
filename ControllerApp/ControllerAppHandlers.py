from ControllerAppSender import ControllerAppSender
from ControllerAppQueue import ControllerAppQueue
from controller.NodeController import NodeController
from ControllerAppConstants import CONTROLLER_QUEUE, FRONTEND_QUEUE, SERVER_IP
from colorama import Fore, Style
import os



class ControllerAppHandlers(object):
    def __init__(self, sender: ControllerAppSender, queue: ControllerAppQueue):
        self.sender = sender
        self.queue = queue
        self.node_controller = NodeController()

    def get_all_nodes(self, args: dict):
        '''
        Recebe os argumentos callback_queue e callback_message
        Manda uma mensagem com um dict dos nodes com seus tempos de processamento controlados pelo controller para a queue desejada
        '''
        callback_queue = args['callback_queue']
        callback_message = args['callback_message']

        self.sender.send_message_to(
            to=callback_queue, 
            message={
                'message': callback_message,
                'args': {
                    'nodes': self.node_controller.get_all_nodes()
                }
            }
        )
    
    def calc_route(self, args: dict):
        '''
        Recebe os argumentos start_node, target_node, algorithm, every_node_callback_message, callback_message callback_queue
        '''
        start_node = args['start_node']
        target_node = args['target_node']
        algorithm = args['algorithm']
        every_node_callback_message = args['every_node_callback_message']
        callback_message = args['callback_message'] 
        callback_queue = args['callback_queue']

        if self.node_controller.has_control_over_nodes(start_node, target_node):
            if algorithm == 'dijkstra':
                algorithm = f'start_{algorithm}'
            
            self.sender.send_message_to(
                to=start_node, 
                message={
                    'message': algorithm,
                    'args': {
                        'target_node': target_node,
                        'every_node_callback_message': every_node_callback_message,
                        'callback_message': callback_message,
                        'callback_queue': callback_queue
                    }
                }
            )
        else:
            print(f'{Fore.RED}This controller app has no control over the nodes {start_node} and {target_node}.{Style.RESET_ALL}')
    
    def create_node(self, args: dict):
        '''
        Cria uma instancia de nó na amazon e mapeia esse nó no banco de dados
        '''
        node_name = args['node_name']
        processing_time = args['processing_time']

        if not self.node_controller.exists(node_name):
            # Cria o registro do nó no banco de dados
            self.node_controller.create_node(node_name, processing_time)
            # TODO - mandar msg pro front subir o container
            os.popen(f'start "cmd" "C:\\Users\\vinic\\Desktop\\TrabFinalSD\\ServerApp\\ServerAppInitialize.py" "{node_name}" "{processing_time}"')
        else:
            print(f'{Fore.RED}Node {node_name} already exist.')

    def connect_nodes(self, args: dict):
        '''
        Conecta dois nós entre si, bidirecionalmente
        '''
        node1 = args['node1']
        node2 = args['node2']
        if self.node_controller.has_control_over_nodes(node1, node2):
            self.node_controller.add_connection_to(node1, node2)
            self.node_controller.add_connection_to(node2, node1)
            self.sender.send_message_to(
                to=node1,
                message={
                    'message': 'connect_to',
                    'args': {
                        'node': node2
                    }
                }
            )
            self.sender.send_message_to(
                to=node2,
                message={
                    'message': 'connect_to',
                    'args': {
                        'node': node1
                    }
                }
            )
        else:
            print(f'{Fore.RED}This controller app has no control over the nodes {node1} and {node2}.{Style.RESET_ALL}')

    def healthcheck(self, args: dict):
        down_nodes = self.node_controller.get_down_nodes()
        for node in down_nodes:
            node_name = node['node_name']
            processing_time = node['processing_time']
            connections = node['connections']
            # TODO - mandar msg pro front subir o container
            os.popen(f'start "cmd" "C:\\Users\\vinic\\Desktop\\TrabFinalSD\\ServerApp\\ServerAppInitialize.py" "{node_name}" "{processing_time}"')
            for connection in connections:
                self.sender.send_message_to(
                    to=node_name, 
                    message={
                        'message': 'connect_to',
                        'args': {
                            'node': connection
                        }
                    }
                )
        
        self.node_controller.reset_all_pinged_back()
        all_nodes = self.node_controller.get_all_node_names()
        for node in all_nodes:
            self.sender.send_message_to(to=node, message='healthcheck')

    def ping_healthcheck(self, args: dict):
        self.node_controller.set_pinged_back(args['node'], True)
