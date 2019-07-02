from ServerAppMapper import ServerAppMapper
from ServerAppSender import ServerAppSender
from ServerAppQueue import ServerAppQueue
from ServerAppConstants import CONTROLLER_QUEUE
from colorama import Fore, Style
from time import sleep, time
from threading import Thread


class ServerAppHandlers(object):
    def __init__(self, sender: ServerAppSender, queue: ServerAppQueue, mapper: ServerAppMapper, listener):
        self.mapper = mapper
        self.sender = sender
        self.queue = queue
        self.listener = listener

    def ping_everyone(self, args: dict):
        '''
        Manda uma mensagem para todos os nós ao qual ele possui o nome
        '''
        nodes = self.mapper.get_connections()
        for node in nodes:
            self.sender.send_message_to('ping', node)

    def ping(self, args: dict):
        print(f'{self.queue.get_queue_name()} pinged.')

    def run_dijkstra(self, args: dict):
        self.try_dijkstra(args)
        try:
            #Thread(target=self.try_dijkstra, args=[args]).start()
            pass
        except Exception as e:
            with open('error.txt', 'a') as out:
                out.write('Cannot handle message. {\'message\': \'dijkstra\', \'args\': ' + args + '} - ' + e + '\n')
            print(f'{Fore.RED}ERRORRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR')
            print('Cannot handle message. {\'message\': \'dijkstra\', \'args\': ' + args + '} - ' + e)
            print(f'{Style.RESET_ALL}')
            sleep(60)

    def try_dijkstra(self, args: dict):
        try:
            self.dijkstra(args)
        except Exception as e:
            with open('error.txt', 'a') as out:
                out.write('Cannot handle message. {\'message\': \'dijkstra\', \'args\': ' + args + '} - ' + e + '\n')
            print(f'{Fore.RED}ERRORRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR')
            print('Cannot handle message. {\'message\': \'dijkstra\', \'args\': ' + args + '} - ' + e)
            print(f'{Style.RESET_ALL}')
            sleep(60)

    def dijkstra(self, args: dict):
        '''
        Algoritmo que é chamado a cada iteração de Dijkstra
        '''
        source_node = args['source']['node']
        source_dist = 0 if args['source']['dist'] is None else args['source']['dist'] + self.queue.get_processing_time()
        target_node = args['target_node']
        visited_nodes = args['visited_nodes']
        every_node_callback_message = args['every_node_callback_message']
        end_algorithm_callback_message = args['end_algorithm_callback_message']
        callback_queue = args['callback_queue']
        pid = args['pid']

        queue_mapper = self.mapper.get_queue_mapper()
        visited_nodes.append(self.queue.get_queue_name())

        self.sender.send_message_to({
            'message': every_node_callback_message,
            'args': {
                'current_node': self.queue.get_queue_name(),
                'total_dist': source_dist,
                'pid': pid,
                'algorithm': 'dijkstra'
            }
        }, callback_queue)

        sleep(3)

        if target_node == self.queue.get_queue_name():
            self.sender.send_message_to({
                'message': end_algorithm_callback_message,
                'args': {
                    'visited_nodes': visited_nodes,
                    'total_dist': source_dist,
                    'reached_end': 1,
                    'pid': pid,
                    'algorithm': 'dijkstra'
                }
            }, callback_queue)
        elif (not source_node in queue_mapper) or (not source_node in queue_mapper) or (queue_mapper[source_node]['dist'] >= source_dist):
            self.mapper.add_to_queue_mapper(source_node, {'dist': source_dist})
            first = True
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
                            'end_algorithm_callback_message': end_algorithm_callback_message,
                            'callback_queue': callback_queue,
                            'pid': pid if first else f'{self.queue.get_queue_name()}{time()}'
                        }
                    }, connection)
                    first = False
        else:
            self.sender.send_message_to({
                'message': end_algorithm_callback_message,
                'args': {
                    'visited_nodes': visited_nodes,
                    'total_dist': source_dist,
                    'reached_end': 0,
                    'pid': pid,
                    'algorithm': 'dijkstra'
                }
            }, callback_queue)
            print(f'{Fore.YELLOW}Dijkstra cannot continue.{Style.RESET_ALL} {args} {self.mapper.get_queue_mapper()}')

    def start_dijkstra(self, args: dict):
        '''
        Handler para a mensagem de inicio do algoritmo de dijkstra
        Espera receber o argumento target_node que é o node ao qual é buscado o menor caminho
        '''
        try:
            target_node = args['target_node']
            self.dijkstra({
                'source': {
                    'node': self.queue.get_queue_name(),
                    'dist': None
                },
                'visited_nodes': [],
                'target_node': target_node,
                'every_node_callback_message': args['every_node_callback_message'],
                'end_algorithm_callback_message': args['end_algorithm_callback_message'],
                'callback_queue': args['callback_queue'],
                'pid': f'{self.queue.get_queue_name()}{time()}'
            })
        except Exception as e:
            with open('error.txt', 'a') as out:
                out.write('Cannot handle message. {\'message\': \'dijkstra\', \'args\': ' + args + '} - ' + e + '\n')
            print(f'{Fore.RED}ERRORRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR')
            print('Cannot handle message. {\'message\': \'dijkstra\', \'args\': ' + args + '} - ' + e)
            print(f'{Style.RESET_ALL}')
            sleep(60)

    def healthcheck(self, args: dict):
        '''
        Toda vez que essa mensagem é chamada, o vértice manda uma mensagem para o controller
        com o intuito de avisar o controller que ainda está rodando
        '''
        self.sender.send_message_to(
            to=CONTROLLER_QUEUE,
            message={
                'message': 'ping_healthcheck',
                'args': {
                    'node': self.queue.get_queue_name()
                }
            }
        )
    
    def kill(self, args: dict):
        '''
        Derruba essa instância
        '''
        print(f'This node is shutting down.')
        self.listener.stop_listening()
        self.queue.self_delete()
        self.queue.close_connection()
