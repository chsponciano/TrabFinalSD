from pika import BlockingConnection, ConnectionParameters
from json import dumps
import sys


# Primeiro argumento é o nome da queue que receberá a mensagem 
# Segundo argumento é o nome do algoritmo
# Dali em diante são os nome dos argumento seguidos do valor dos argumento
# Por exemplo, para iniciar Dijkstra no nó q1 com o target_node sendo q5:
# q1 dijkstra target_node q5

args = sys.argv[1:]

queue = args[0]
algorithm = args[1]
algorithm_args = {'message': algorithm, 'args': {}}

del args[0]
del args[0]

arg_name = None
arg_value = None
for arg in args:
    if arg_name is None:
        arg_name = arg
    else:
        arg_value = arg

        algorithm_args['args'][arg_name] = arg_value

        arg_name = None
        arg_value = None

connection = BlockingConnection(ConnectionParameters('localhost'))
channel = connection.channel()
channel.basic_publish(exchange='', routing_key=queue, body=dumps(algorithm_args))
channel.close()
