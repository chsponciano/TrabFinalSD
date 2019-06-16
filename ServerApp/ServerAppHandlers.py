from ServerAppMapper import ServerAppMapper
from ServerAppSender import ServerAppSender
from ServerAppQueue import ServerAppQueue


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
