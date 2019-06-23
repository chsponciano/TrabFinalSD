from ClientAppSender import ClientAppSender
from ClientAppQueue import ClientAppQueue
from ClientAppConstants import CONTROLLER_QUEUE
from colorama import Fore, Style
from arquivo_fodasse_no_front import func_que_realmente_atualiza_a_lista_de_nos


class ClientAppHandlers(object):
    def __init__(self, sender: ClientAppSender, queue: ClientAppQueue, listener):
        self.sender = sender
        self.queue = queue
        self.listener = listener

    def receive_all_nodes(self, args: dict):
        '''
        Recebe somente o argumento nodes
        '''
        # Esse método é acionado com o retorno daquela mensagem de get_all_nodes
        # A lista de nós atualizada vem nos argumentos
        # Nesse caso é o unico algumento passado
        
        # Foi mandado com o nome de 'nodes' por isso a linha abaixo
        nodes = args['nodes']

        # Chama a função do front que atualiza a lista de nos
        func_que_realmente_atualiza_a_lista_de_nos(nodes)

    def every_node_callback_message(self, args: dict):
        '''
        Vai pingar todas vez que passar por um nó na execução do algoritmo de dijkstra
        '''
        current_node = args['current_node']
        total_dist = args['total_dist']

    def end_algorithm_callback_message(self, args: dict):
        '''
        Vai pingar aqui no final do algoritmo de dijkstra.
        Lembrando que pode pingar aqui varias vezes dependendo do grafo. Por isso deve-se manter um estado
        indicando qual o menor caminho de todos
        '''
        visited_nodes = args['visited_nodes']
        total_dist = args['total_dist']

    def calc_route(self, args: dict):
        '''
        Vai pingar aqui assim que o algoritmo deseja estiver começado
        '''
        algorithm: args['algorithm']
        success: args['success']

    def create_node(self, args: dict):
        '''
        Vai pingar aqui quando a criação de um novo nó foi requisitada e ele foi criado no banco de dados e deve ser subido na amazon
        ou quando a rotina de healthcheck notar que um vértice caiu e precisar ser reiniciado
        '''
        node_name = args['node_name']
        processing_time = args['processing_time']
        success = args['success']

    def delete_node(self, args: dict):
        '''
        Recebe o retorno da mensagem delete_node
        '''
        node_name = args['node']['node_name']
        connections = args['node']['connections']
        success = args['success']

    def create_connection(self, args: dict):
        '''
        Recebe o retorno da mensagem create_connection
        '''
        node1 = args['node1']
        node2 = args['node2']
        success = args['success']

    def delete_connection(self, args: dict):
        '''
        Recebe o retorno da mensagem delete_connection
        '''
        node1 = args['node1']
        node2 = args['node2']
        success = args['success']

        
