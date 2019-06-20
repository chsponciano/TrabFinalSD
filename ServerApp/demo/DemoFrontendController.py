from pika import BlockingConnection, ConnectionParameters
from json import dumps


connection = BlockingConnection(ConnectionParameters('localhost'))
channel = connection.channel()

channel.basic_publish(exchange='', routing_key='q1', body=dumps({'message':'start_dijkstra', 'args':{'target_node':'q5'}}))
