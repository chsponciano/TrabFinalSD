from ServerAppMapper import ServerAppMapper
from ServerAppSender import ServerAppSender
from ServerAppQueue import ServerAppQueue
from ServerAppConstants import *
from colorama import Fore, Style


class ServerAppHandlers(object):
    def __init__(self, sender: ServerAppSender, queue: ServerAppQueue, mapper: ServerAppMapper):
        self.mapper = mapper
        self.sender = sender
        self.queue = queue

    def connect_to(self, args: dict):
        '''
        Se conecta com o nó requisitado
        É feita somente uma conexão unidirecional, se o nó enviado no args deve conhece esse nó também, ele deverá receber a mensma mensagem
        '''
        node = args['node']
        self.mapper.connect_to(node)
        print(
            f'Connection between nodes {self.queue.get_queue_name()} and {node} has been established.')

    def ping_everyone(self, args: dict):
        '''
        Manda uma mensagem para todos os nós ao qual ele possui o nome
        '''
        nodes = self.mapper.get_connections()
        for node in nodes:
            self.sender.send_message_to('ping', node)

    def ping(self, args: dict):
        print(f'{self.queue.get_queue_name()} pinged.')

    def dijkstra(self, args: dict):
        '''
        Algoritmo que é chamado a cada iteração de Dijkstra
        '''
        source_node = args['source']['node']
        source_dist = args['source']['dist'] + 1
        target_node = args['target_node']
        visited_nodes = args['visited_nodes']

        queue_mapper = self.mapper.get_queue_mapper()
        visited_nodes.append(self.queue.get_queue_name())

        if target_node == self.queue.get_queue_name():
            self.sender.send_message_to({
                'message': 'dijkstra_done',
                'args': {
                    'visited_nodes': visited_nodes,
                    'total_dist': source_dist
                }
            }, source_node)
        elif (not source_node in queue_mapper) or (queue_mapper[source_node]['dist'] >= source_dist):
            self.mapper.add_to_queue_mapper(source_node, {'dist': source_dist})
            for connection in self.mapper.get_connections():
                if not connection in visited_nodes:
                    self.sender.send_message_to({
                        'message': 'dijkstra',
                        'args': {
                            'source': {
                                'node': source_node,
                                'dist': source_dist
                            },
                            'visited_nodes': visited_nodes,
                            'target_node': target_node
                        }
                    }, connection)
        else:
            print(
                f'Dijkstra cannot continue {args} {self.mapper.get_queue_mapper()}')

    def start_dijkstra(self, args: dict):
        '''
        Handler para a mensagem de inicio do algoritmo de Dijkstra
        Espera receber somente o argumento target_node que é o node ao qual é buscado o menor caminho
        '''
        self.dijkstra({
            'source': {
                'node': self.queue.get_queue_name(),
                'dist': -1
            },
            'visited_nodes': [],
            'target_node': args['target_node']
        })

    def dijkstra_done(self, args: dict):
        '''
        Handler para a mensagem enviada indicando o fim do algoritmo
        Nesse caso é um handler placeholder, já que na impl final esse handler deverá estar no app frontend
        '''
        print(f'dijkstra_done: {args}')
