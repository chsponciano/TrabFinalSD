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
    
    def teste(self, args: dict):
        print(f'Mensagem teste recebida! args: {args}')

    def first_connect(self, args: dict):
        '''
        Recebe a primeira mensagem enviada por uma nova instancia.
        Adiciona a nova instancia em sua lista de conexões.
        Envia uma mensagem para essa instancia para ser adicionada na lista de conexões dela
        '''
        sender = args['sender_queue_name']
        if not self.mapper.is_connected_to(sender):
            self.mapper.connect_to(sender)
            print(f'Connection between nodes {self.queue.get_queue_name()} and {sender} has been established.')
            message = {
                'message': 'connect_to',
                'args': {
                    'node': self.queue.get_queue_name()
                }
            }
            self.sender.send_message_to(message, to=sender)
            print(f'Requesting {sender} to add {self.queue.get_queue_name()} to it\'s list of conections.')
        else:
            raise Exception()

    def connect_to(self, args: dict):
        '''
        Se conecta com o nó requisitado
        '''
        node = args['node']
        self.mapper.connect_to(node)
        print(f'Connection between nodes {self.queue.get_queue_name()} and {node} has been established.')

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
            print(f'Dijkstra cannot continue {args} {self.mapper.get_queue_mapper()}')
    

    def start_dijkstra(self, args: dict):
        self.dijkstra({
            'source': {
                'node': self.queue.get_queue_name(),
                'dist': -1
            },
            'visited_nodes': [],
            'target_node': args['target_node']
        })

    def dijkstra_done(self, args: dict):
        print(f'dijkstra_done: {args}')
