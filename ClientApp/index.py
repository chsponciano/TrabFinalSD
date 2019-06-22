from flask import Flask, render_template, request, redirect, session, flash, url_for
import subprocess
import pickle
from node import Node

app = Flask(__name__)
contador = 1
dict_nodes = dict()
file_seralization = 'graph.dat'

@app.route('/')
def index():
    get_dict()
    return render_template('index.html')

@app.route('/add', methods=['POST',])
def add_server():
    global contador
    global dict_nodes
    idx = str(request.form['id_server'] + "_" + str(contador))
    dict_nodes.update({idx, Node(idx, str(request.form['cust_server']))})
    contador += 1
    save_dict()

@app.route('/stop', methods=['POST',])
def stop_server():
    global dict_nodes
    dict_nodes.get(str(request.form['id_server'])).stop()
    save_dict()

@app.route('/start', methods=['POST',])
def start_server():
    global dict_nodes
    dict_nodes.get(str(request.form['id_server'])).start()
    save_dict()

@app.route('/route', methods=['POST',])
def calc_router():
    node1 = request.form['node_one_server']
    node2 = request.form['node_two_server']
    algorithm = request.form['algorithm_server']
    print(f'{node1} - {node2} - {algorithm}')

def save_dict():
    global file_seralization
    global dict_nodes
    fl = open(file_seralization, 'wb')
    pickle.dump(dict_nodes, fl)
    fl.close()

def get_dict():
    global file_seralization
    global dict_nodes
    fl = open(file_seralization, 'rb')
    dict_nodes.update({pickle.load(fl)})
    fl.close()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
