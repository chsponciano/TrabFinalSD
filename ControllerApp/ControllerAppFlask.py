from flask import Flask, render_template, request, redirect, session, flash, url_for
from flask_socketio import SocketIO, send, emit
from NodeController import NodeController
from ControllerAppConstants import CONTROLLER_QUEUE
from ControllerAppQueue import ControllerAppQueue
from ControllerAppListener import ControllerAppListener
from colorama import Fore, Style
from flask import jsonify
from time import time
import os
import math


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
        amazon.delete_instance(node)
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

        SOCKET_QUEUE = f'SQ{time()}'
        args['callback_queue'] = SOCKET_QUEUE
        every_node_callback_message_to_frontend = args['every_node_callback_message']
        end_algorithm_callback_message_to_frontend = args['end_algorithm_callback_message']
        args['every_node_callback_message'] = 'every_node_callback_message'
        args['end_algorithm_callback_message'] = 'end_algorithm_callback_message'
        args['algorithm'] = 'dijkstra'
        threads_of_messages = {}

        if node_controller.has_control_over_nodes(args['start_node'], args['target_node']):
            handlers = {
                'every_node_callback_message': lambda args: every_node_callback_message(args, every_node_callback_message_to_frontend, threads_of_messages),
                'end_algorithm_callback_message': lambda args: end_algorithm_callback_message(args, listener, queue, end_algorithm_callback_message_to_frontend, threads_of_messages),
            }
            queue = ControllerAppQueue(queue_name=SOCKET_QUEUE)
            print(f'Temp queue with name {SOCKET_QUEUE} created.')
            listener = ControllerAppListener(queue=queue, queue_name=SOCKET_QUEUE, message_handler_mapper=handlers)
            
            sender.send_message_to(
                to=CONTROLLER_QUEUE,
                message={
                    'message': 'calc_route',
                    'args': args
                }
            )
            success = 1
        else: 
            success = 0
    except Exception as e:
        success = 0
        print('Exception')
        print(e)
    
    message = args['callback_message']
    args = {
        'algorithm': args['algorithm'],
        'success': success
    }
    print(f'Emiting {message} with value {args} via socket back to client.')
    emit(message, args)
    if listener is not None:
        listener.start_listening()

def every_node_callback_message(args, message, threads_of_messages):
    print(f'In - {message}: Threads of messages is {threads_of_messages}.')
    # Update the status of the pid in question on the dictionary of threads
    if not args['pid'] in threads_of_messages:
        threads_of_messages[args['pid']] = {}
    threads_of_messages[args['pid']]['active'] = 1
    threads_of_messages[args['pid']]['args'] = args
    
    # Deletes useless information for the frontend
    if 'pid' in args:
        del args['pid']

    print(f'Out - {message}: Threads of messages is {threads_of_messages}.')
    # Emits a message with the arguments via socket
    print(f'Emiting {message} with value {args} via socket back to client.')
    emit(message, args)

def end_algorithm_callback_message(args, listener, queue, message, threads_of_messages):
    print(f'In - {message}: Threads of messages is {threads_of_messages}.')
    # Update the status of the pid in question on the dictionary of threads
    if not args['pid'] in threads_of_messages:
        threads_of_messages[args['pid']] = {}
    threads_of_messages[args['pid']]['active'] = 0
    threads_of_messages[args['pid']]['reached_end'] = args['reached_end']
    threads_of_messages[args['pid']]['args'] = args

    # Figures it out if theres is at leat one active process running in the algorithim 
    any_active = False
    for pid in threads_of_messages:
        any_active = any_active or threads_of_messages[pid]['active'] is 1
    
    if not any_active:
        # Finds the process that reached the target node with the least total distance
        smallest_dist = {'total_dist': math.inf}
        for pid in threads_of_messages:
            thread_of_messages = threads_of_messages[pid]
            if 'reached_end' in thread_of_messages and thread_of_messages['reached_end'] is 1 and thread_of_messages['args']['total_dist'] < smallest_dist['total_dist']:
                smallest_dist = thread_of_messages['args']
        
        # Deletes useless information for the frontend
        if 'pid' in smallest_dist:
            del smallest_dist['pid']
        if 'reached_end' in smallest_dist:
            del smallest_dist['reached_end']

        if smallest_dist['total_dist'] is math.inf:
            smallest_dist = {'message': 'The alghorithim couldn\'t come to an end becauce boths nodes are not connected.'}

        # Emits the final message via socket and kill's the temp queue
        print(f'Emiting {message} with value {smallest_dist} via socket back to client.')
        emit(message, smallest_dist)
        listener.stop_listening()
        queue.self_delete()
        queue.close_connection()
        print(f'Queue {queue.get_queue_name()} and it\'s listener were killed.')
    print(f'Out - {message}: Threads of messages is {threads_of_messages}.')

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
    socketio.run(app, debug=True, port=80, host='0.0.0.0')