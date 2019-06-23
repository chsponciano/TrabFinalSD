from ClientAppSender import ClientAppSender
from ClientAppListener import ClientAppListener
from ClientAppQueue import ClientAppQueue
from ClientAppConstants import FRONTEND_QUEUE
from colorama import init, Fore


# RECEBIMENTO DE MENSAGENS

# No arquivo ClientAppListener vc define a "interface" de mensagens, adicionando novas keys/values no método get_default_message_handler_mapper
# de lá vc vai ver que ele chama os métodos da classe ClientAppListener, é lá que vc implementa o que fazer com cada mensagem
# nessa classe vc vai encontrar todas as mensagens que o controller chama no front


# ENVIO

# Vc vai usar a classe ClientAppSender pra enviar as mensagens. Atraves do método send_message_to, passagndo uma mensagem em formato de dict
# {'message': 'NOME_DA_MENSAGEM', 'args': {/*outro dict com argumentos*/}}
# e o nome da fila que vc quer se comunicar, no caso vc vai usar a constante CONTROLLER_QUEUE
# vc pode mandar as mensagens a partir de qualquer lugar do código

# as mensagens que vc pode enviar são:
# {'message': 'get_all_nodes', 'args': {'callback_queue': 'QUEUE_NAME', 'callback_message': 'MESSAGE_NAME'}}
# {'message': 'calc_route', 'args': {'start_node': 'NODE_NAME', 'target_node': 'NODE_NAME', 'algorithm': 'dijkstra', 'every_node_callback_message': 'MESSAGE_NAME', 'callback_message': 'MESSAGE_NAME', 'callback_queue': 'FRONTEND_QUEUE'}}
# {'message': 'create_node', 'args': {'node_name': 'NODE_NAME', 'processing_time': 'PROCESSING_TIME'}}
# {'message': 'connect_nodes', 'args': {'node1': 'NODE_NAME', 'node2': 'NODE_NAME'}}
# {'message': 'delete_connection', 'args': {'node1': 'NODE_NAME', 'node2': 'NODE_NAME'}}
# {'message': 'delete_node', 'args': {'node': 'NODE_NAME'}}
# {'message': 'kill', 'args': {'kill_all': 0}}  # Vc manda 0 pra false e qualquer outro numero pra true # kill_all mata todas as aplicações dos vértices

init()

# As classes instanciadas abaixo devem ser instancias somente uma vez durante a aplicação

queue = ClientAppQueue()
sender = ClientAppSender(queue)
listener = ClientAppListener(queue, sender)

listener.start_listening_async()

print(f'{FRONTEND_QUEUE} initialized.')
