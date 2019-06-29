from flask import Flask 
from flask_socketio import SocketIO, send, emit
from time import sleep
from threading import Thread



app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
socketio = SocketIO(app, async_mode='threading')
aux = True


def aux_met():
    while True:
        sleep(5)
        print('Please')
        try:
                emit('vai_demonio', 'Caralho funfa, finalmente!')
        except:
                print('Exception')


@socketio.on('message')
def handleMessage(msg):
    print('Message: ' + msg)
    send(msg, broadcast=True)
    

print('iniciando')
if __name__ == '__main__':
        socketio.start_background_task(target=aux_met)
        socketio.run(app)
print('iniciou')

