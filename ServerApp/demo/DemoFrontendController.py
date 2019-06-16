from pika import BlockingConnection, ConnectionParameters
from json import dumps


connection = BlockingConnection(ConnectionParameters('localhost'))
channel = connection.channel()

channel.basic_publish(exchange='', routing_key='TYPE_QUEUE_NAME_HERE', body=dumps({'message':'TYPE_OF_MESSAGE', 'args':{'ARGS_TO':'SEND'}}))
