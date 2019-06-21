from pika import BlockingConnection, ConnectionParameters
from json import dumps


connection = BlockingConnection(ConnectionParameters('IP_DA_FILA'))
channel = connection.channel()

channel.basic_publish(
    exchange='', 
    routing_key='FILA_QUE_RECEBE_A_MENSAGEM', 
    body=dumps({
        'message':'TIPO_DA_MENSAGEM', 
        'args':{
            'ARG_QUALQUER':'VALOR_DO_ARG'
        }
    })
)
