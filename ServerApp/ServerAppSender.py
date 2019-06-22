from json import dumps


class ServerAppSender(object):
    def __init__(self, server_app_queue):
        self.server_app_queue = server_app_queue

    def send_message_to(self, message, to: str):
        message = self.prepare_message(message)
        print(f'Sending {message} to {to}')
        self.server_app_queue.get_channel().basic_publish(
            exchange='', routing_key=to, body=message)

    def prepare_message(self, message):
        if isinstance(message, dict):
            if not 'message' in message:
                raise Exception()
            if not 'args' in message:
                message['args'] = {}
            message = dumps(message)

        elif isinstance(message, str):
            message = dumps({'message': message, 'args': {}})
        else:
            raise Exception()
        return message
