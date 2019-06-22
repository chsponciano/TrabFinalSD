from pika import BlockingConnection, ConnectionParameters
from json import dumps
import sys

args = sys.argv[1:]

connection = BlockingConnection(ConnectionParameters('18.191.149.251'))
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
