from ControllerAppSender import ControllerAppSender
from ControllerAppQueue import ControllerAppQueue
from ControllerAppTaskScheduler import ControllerAppTaskScheduler
from NodeController import NodeController
from ControllerAppConstants import CONTROLLER_QUEUE, FRONTEND_QUEUE, RABBIT_HOST
from colorama import Fore, Style
import os


class ControllerAppHandlers(object):
    def __init__(self, sender, queue, task_scheduler, listener, node_controller, amazon):
        self.sender = sender
        self.queue = queue
        self.listener = listener
        self.task_scheduler = task_scheduler
        self.node_controller = node_controller
        self.amazon = amazon

    def calc_route(self, args: dict):
        '''
        Recebe os argumentos start_node, target_node, algorithm, every_node_callback_message, callback_queue
        '''
        start_node = args['start_node']
        target_node = args['target_node']
        algorithm = args['algorithm']
        every_node_callback_message = args['every_node_callback_message']
        end_algorithm_callback_message = args['end_algorithm_callback_message']
        callback_queue = args['callback_queue']

        try:
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
                            'end_algorithm_callback_message': end_algorithm_callback_message,
                            'callback_queue': callback_queue
                        }
                    }
                )
            else:
                print(f'{Fore.RED}This controller app has no control over the nodes {start_node} and {target_node}.{Style.RESET_ALL}')
        except:
            pass

    def healthcheck(self, args: dict):
        down_nodes = self.node_controller.get_down_nodes()
        for node in down_nodes:
            node_name = node['node_name']
            processing_time = node['processing_time']
            connections = node['connections']
            self.sender.send_message_to(
                to=FRONTEND_QUEUE,
                message={
                    'message': 'create_node',
                    'args': {
                        'node_name': node_name,
                        'processing_time': processing_time
                    }
                }
            )
            self.amazon.new_instance(node_name, processing_time)
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

    def kill(self, args: dict):
        print(f'This controller is shutting down.')
        if 'kill_all' in args and args['kill_all'] != 0:
            all_nodes = self.node_controller.get_all_node_names()
            for node in all_nodes:
                print(f'Shutting down node {node}.')
                self.sender.send_message_to(to=node, message='kill')
        self.task_scheduler.shut_down()
        self.listener.stop_listening()
        self.queue.close_connection()

