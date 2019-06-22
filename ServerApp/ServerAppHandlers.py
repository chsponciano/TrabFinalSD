from ServerAppMapper import ServerAppMapper
from ServerAppSender import ServerAppSender
from ServerAppQueue import ServerAppQueue
from ServerAppConstants import CONTROLLER_QUEUE
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
        '''
        Algoritmo que é chamado a cada iteração de Dijkstra
        '''
        source_node = args['source']['node']
        source_dist = 0 if args['source']['dist'] is None else args['source']['dist'] + self.queue.get_processing_time()
        target_node = args['target_node']
        visited_nodes = args['visited_nodes']
        every_node_callback_message = args['every_node_callback_message']
        callback_message = args['callback_message']
        callback_queue = args['callback_queue']

        queue_mapper = self.mapper.get_queue_mapper()
        visited_nodes.append(self.queue.get_queue_name())

        self.sender.send_message_to({
            'message': every_node_callback_message,
            'args': {
                'current_node': self.queue.get_queue_name(),
                'total_dist': source_dist
            }
        }, callback_queue)

        if target_node == self.queue.get_queue_name():
            # TODO - ping_dijkstra done no controller
            self.sender.send_message_to({
                'message': callback_message,
                'args': {
                    'visited_nodes': visited_nodes,
                    'total_dist': source_dist
                }
            }, callback_queue)
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
                            'target_node': target_node,
                            'every_node_callback_message': every_node_callback_message,
                            'callback_message': callback_message,
                            'callback_queue': callback_queue
                        }
                    }, connection)
        else:
            print(f'{Fore.YELLOW}Dijkstra cannot continue.{Style.RESET_ALL} {args} {self.mapper.get_queue_mapper()}')

    def start_dijkstra(self, args: dict):
        '''
        Handler para a mensagem de inicio do algoritmo de dijkstra
        Espera receber o argumento target_node que é o node ao qual é buscado o menor caminho
        '''
        target_node = args['target_node']
        self.dijkstra({
            'source': {
                'node': self.queue.get_queue_name(),
                'dist': None
            },
            'visited_nodes': [],
            'target_node': target_node,
            'every_node_callback_message': args['every_node_callback_message'],
            'callback_message': args['callback_message'],
            'callback_queue': args['callback_queue']
        })

    def dijkstra_done(self, args: dict):
        '''
        Handler para a mensagem enviada indicando o fim do algoritmo
        Nesse caso é um handler placeholder, já que na impl final esse handler deverá estar no app frontend
        '''
        print(f'dijkstra_done: {args}')

    def healthcheck(self, args: dict):
        self.sender.send_message_to(
            to=CONTROLLER_QUEUE,
            message={
                'message': 'ping_healthcheck',
                'args': {
                    'node': self.queue.get_queue_name()
                }
            }
        )
