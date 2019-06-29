from flask import Flask, render_template, request, redirect, session, flash, url_for
from flask_socketio import SocketIO, send, emit
from NodeController import NodeController
from ControllerAppConstants import CONTROLLER_QUEUE
from ControllerAppQueue import ControllerAppQueue
from ControllerAppListener import ControllerAppListener
from colorama import Fore, Style
from flask import jsonify
import os


# get_all_nodes
# create_node
# delete_node
# create_connection
# delete_connection

# calc_router
# every_node_callback_message
# end_algorithm_callback_message

app = Flask(__name__)
socketio = SocketIO(app)
node_controller = None
sender = None
amazon = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_all_nodes', methods=['GET'])
def get_all_nodes():
    global node_controller
    return jsonify(node_controller.get_all_nodes() )

@app.route('/create_node', methods=['POST'])
def create_node():
    global node_controller
    global amazon
    node_name = request.form['node_name']
    processing_time = request.form['processing_time']
    if not node_controller.exists(node_name):
        # Cria o registro do nó no banco de dados
        node_controller.create_node(node_name, processing_time)
        amazon.new_instance(node_name, processing_time)
        success = 1
    else:
        success = 0
        print(f'{Fore.RED}Node {node_name} already exist.')
    return jsonify(
            {
                'node_name': node_name,
                'processing_time': processing_time,
                'success': success
            }
    )

@app.route('/create_connection', methods=['POST'])
def create_connection():
    global node_controller
    global sender
    node1 = request.form['node1']
    node2 = request.form['node2']
    if node_controller.has_control_over_nodes(node1, node2):
        node_controller.add_connection_to(node1, node2)
        node_controller.add_connection_to(node2, node1)
        sender.send_message_to(
            to=node1,
            message={
                'message': 'connect_to',
                'args': {
                    'node': node2
                }
            }
        )
        sender.send_message_to(
            to=node2,
            message={
                'message': 'connect_to',
                'args': {
                    'node': node1
                }
            }
        )
        success = 1
    else:
        success = 0
        print(f'{Fore.RED}This controller app has no control over the nodes {node1} and {node2}.{Style.RESET_ALL}')
    return jsonify(
            {
                'node1': node1,
                'node2': node2,
                'success': success
            }
    )

@app.route('/delete_connection', methods=['POST'], )
def delete_connection():
    global node_controller
    global sender
    node1 = request.form['node1']
    node2 = request.form['node2']
    try:
        node_controller.delete_connection(node1, node2)
        node_controller.delete_connection(node2, node1)
        sender.send_message_to(
            to=node1,
            message={
                'message': 'delete_connection',
                'args': {
                    'connection': node2
                }
            }
        )
        sender.send_message_to(
            to=node2,
            message={
                'message': 'delete_connection',
                'args': {
                    'connection': node1
                }
            }
        )
        success = 1
    except:
        success = 0
    return jsonify(
            {
                'node1': node1,
                'node2': node2,
                'success': success
            }
    )

@app.route('/delete_node', methods=['POST'])
def delete_node():
    global node_controller
    global sender
    node = request.form['node']
    try:
        connections = node_controller.get_all_connections(node)
        node_controller.delete_node(node)
        for connection in connections:
            sender.send_message_to(
                to=connection,
                message={
                    'message': 'delete_connection',
                    'args': {
                        'connection': node
                    }
                }
            )
        sender.send_message_to(to=node, message='kill')
        success = 1
    except:
        success = 0
    return jsonify(
            {
                'node': {
                    'node_name': node,
                    'connections': connections
                },
                'success': success
            }
    )

@app.route('/kill', methods=['POST'])
def kill():
    global sender
    kill_all = request.form['kill_all']
    sender.send_message_to(
        to=CONTROLLER_QUEUE,
        message={
            'message': 'kill',
            'args': {
                'kill_all': kill_all
            }
        }
    )

@socketio.on('calc_route')
def calc_route(args):
    print(f'{Fore.RED}Socket message: {args}{Style.RESET_ALL}')

    listener = None

    try:
        global sender
        global node_controller

        SOCKET_QUEUE = 'queue_do_socket'
        args['callback_queue'] = SOCKET_QUEUE
        every_node_callback_message_to_frontend = args['every_node_callback_message']
        end_algorithm_callback_message_to_frontend = args['end_algorithm_callback_message']
        args['every_node_callback_message'] = 'every_node_callback_message'
        args['end_algorithm_callback_message'] = 'end_algorithm_callback_message'
        args['algorithm'] = 'dijkstra'

        if node_controller.has_control_over_nodes(args['start_node'], args['target_node']):
            handlers = {
                'every_node_callback_message': 
lambda args: print(f'{every_node_callback_message_to_frontend} - {args} - {emit(every_node_callback_message_to_frontend, args)}'),
                'end_algorithm_callback_message': 
lambda args: print(f'{end_algorithm_callback_message_to_frontend} - {args} - {emit(end_algorithm_callback_message_to_frontend, args)} - {listener.stop_listening()} - {queue.self_delete()} - {queue.close_connection()}')
            }
            queue = ControllerAppQueue(queue_name=SOCKET_QUEUE)
            listener = ControllerAppListener(queue=queue, queue_name=SOCKET_QUEUE, message_handler_mapper=handlers)
            
            sender.send_message_to(
                to=CONTROLLER_QUEUE,
                message={
                    'message': 'calc_route',
                    'args': args
                }
            )
            print('#'*150)
            success = 1
        else: 
            success = 0
    except Exception as e:
        success = 0
        print('Exception')
        print(e)
    
    emit(
        args['callback_message'], 
        {
            'algorithm': args['algorithm'],
            'success': success
        }
    )
    if listener is not None:
        listener.start_listening()

def add_node_controller(nc):
    global node_controller
    node_controller = nc

def add_sender(s):
    global sender
    sender = s

def add_amazon(a):
    global amazon
    amazon = a

def run():
    global app
    global socketio
    
    app.config['SECRET_KEY'] = 'mysecret'
    socketio.run(app, debug=True)
