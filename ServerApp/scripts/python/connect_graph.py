from pika import BlockingConnection, ConnectionParameters
from json import dumps
import sys


# Recebe as conexão a serem feitas em par
# q1 q2 q1 q3 
# Foramará um grafo onde q1 conhece q2 e q3, porém q2 não conhece q3

args = sys.argv[1:]

connection = BlockingConnection(ConnectionParameters('localhost'))
channel = connection.channel()

q1 = None
q2 = None
for arg in args:
    if q1 is None:
        q1 = arg
    else:
        q2 = arg

        channel.basic_publish(
            exchange='', 
            routing_key=q1, 
            body=dumps({
                'message':'connect_to', 
                'args':{
                    'node':q2
                }
            })
        )

        channel.basic_publish(
            exchange='', 
            routing_key=q2,
            body=dumps({
                'message':'connect_to', 
                'args':{
                    'node':q1
                }
            })
        )

        q2 = None
        q1 = None

channel.close()
