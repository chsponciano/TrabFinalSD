from pika import BlockingConnection, ConnectionParameters
from json import dumps


connection = BlockingConnection(ConnectionParameters('localhost'))
channel = connection.channel()
# qd_content = channel.queue_declare(queue="controller-queue",passive=True)

callback_queue = 'teste-controller'
callback_message = 'teste-message'
calc_route = {
    'start_node': 'q1',
    'target_node': 'q2',
    'algorithm': 'dijkstra',
    'every_node_callback_message': callback_message,
    'callback_message': callback_message,
    'callback_queue': callback_queue
}

get_all_nodes = {
    'callback_queue': callback_queue,
    'callback_message': callback_message
}

create_node = {
    'node_name': 'q6',
    'processing_time': '3'
}

connect_nodes = {
    'node1': 'q4',
    'node2': 'q6'
}

delete_node = {
    'node': 'q6'
}

delete_connection = {
    'node1': 'q6',
    'node2': 'q4'
}

message = {
    'message': 'kill',
    'args': {
        'kill_all': '1'
    }
}

channel.basic_publish(exchange='', routing_key='controller-queue', body=dumps(message))

channel.close()


