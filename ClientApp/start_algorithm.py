from pika import BlockingConnection, ConnectionParameters
from json import dumps
import sys

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

connection = BlockingConnection(ConnectionParameters('18.191.149.251'))
channel = connection.channel()
channel.basic_publish(exchange='', routing_key=queue, body=dumps(algorithm_args))
channel.close()
