from messenger.ClientAppInitialize import ClientAppInitialize
from messenger.ClientAppConstants import CONTROLLER_QUEUE, FRONTEND_QUEUE


client_app = ClientAppInitialize()


def func_do_front_que_atualiza_lista_de_nos():
    # Quando o cara clica no botão de atulizar a lista de nós, deve ser acionado esse método
    # Faz umas animações no front pra mostrar que ta carregando

    # Cria uma mensagem pro controller, pedindo pra ele acionar uma mensagem do front com a lista de nós que ele tem
    message = {
        'message': 'get_all_nodes',
        'args': {
            'callback_message': 'receive_all_nodes',
            'callback_queue': FRONTEND_QUEUE
        }
    }
    # Manda a mensagem pro controller
    client_app.sender.send_message_to(to=CONTROLLER_QUEUE, message=message)
    
    # Segue a vida
    # Vc mandou uma mensagem e agora vai esperar o retorno 

    # no caso como foi mandado o argumento callback_message como receive_all_nodes
    # o retorno vai acontecer nesse método, na classe ClientAppHandlers linha 13

    # dai vc deixa uma animação de loading, pra dizer que ta esperando o retorno do controller 

def func_que_realmente_atualiza_a_lista_de_nos(lista_de_nos_atualizada: list):
    # Método que é acionado pela classe de handlers com o retorno do controller
    # Aqui vc de fato atualiza a lista de nós na tela
    print(lista_de_nos_atualizada)
