from ClientAppSender import ClientAppSender
from ClientAppQueue import ClientAppQueue
from ClientAppConstants import CONTROLLER_QUEUE
from colorama import Fore, Style


class ClientAppHandlers(object):
    def __init__(self, sender: ClientAppSender, queue: ClientAppQueue, listener):
        self.sender = sender
        self.queue = queue
        self.listener = listener

    def receive_all_nodes(self, args: dict):
        '''
        Recebe somente o argumento nodes
        '''
        nodes = args['nodes']

    def every_node_callback_message_dijkstra(self, args: dict):
        '''
        Vai pingar todas vez que passar por um nó na execução do algoritmo de dijkstra
        '''
        current_node = args['current_node']
        total_dist = args['total_dist']

    def callback_message_dijkstra(self, args: dict):
        '''
        Vai pingar aqui no final do algoritmo de dijkstra.
        Lembrando que pode pingar aqui varias vezes dependendo do grafo. Por isso deve-se manter um estado
        indicando qual o menor caminho de todos
        '''
        visited_nodes = args['visited_nodes']
        total_dist = args['total_dist']

    def create_node(self, args: dict):
        '''
        Vai pingar aqui quando a criação de um novo nó foi requisitada e ele foi criado no banco de dados e deve ser subido na amazon
        ou quando a rotina de healthcheck notar que um vértice caiu e precisar ser reiniciado
        '''
        node_name = args['node_name']
        processing_time = args['processing_time']

    