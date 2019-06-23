from pika import BlockingConnection, ConnectionParameters
from json import dumps


connection = BlockingConnection(ConnectionParameters('localhost'))
channel = connection.channel()
# qd_content = channel.queue_declare(queue="controller-queue",passive=True)

callback_queue = 'teste-controller'
callback_message = 'teste-message'
calc_route = {
    'start_node': 'q1',
    'target_node': 'q4',
    'algorithm': 'dijkstra',
    'every_node_callback_message': callback_message,
    'end_algorithm_callback_message': callback_message,
    'callback_message': callback_message,
    'callback_queue': callback_queue
}

get_all_nodes = {
    'callback_queue': callback_queue,
    'callback_message': callback_message
}

create_node = {
    'node_name': 'q6',
    'processing_time': '3',
    'callback_queue': callback_queue,
    'callback_message': callback_message
}

create_connection = {
    'node1': 'q4',
    'node2': 'q3',
    'callback_queue': callback_queue,
    'callback_message': callback_message
}

delete_node = {
    'node': 'q5',
    'callback_queue': callback_queue,
    'callback_message': callback_message
}

delete_connection = {
    'node1': 'q4',
    'node2': 'q',
    'callback_queue': callback_queue,
    'callback_message': callback_message
}

message = {
    'message': 'calc_route',
    'args': calc_route
}

channel.basic_publish(exchange='', routing_key='controller-queue', body=dumps(message))

channel.close()


