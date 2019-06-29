from ClientAppConstants import SUPPRESS_LOG_SENDER
from json import dumps


class ClientAppSender(object):
    def __init__(self, queue):
        self.queue = queue

    def send_message_to(self, message, to: str):
        message = self.prepare_message(message)
        if not message['message'] in SUPPRESS_LOG_SENDER:
            print(f'Sending {message} to {to}')
        self.queue.get_channel().basic_publish(exchange='', routing_key=to, body=dumps(message))

    def prepare_message(self, message):
        if isinstance(message, dict):
            if not 'message' in message:
                raise Exception()
            if not 'args' in message:
                message['args'] = {}
            message = message

        elif isinstance(message, str):
            message = {'message': message, 'args': {}}
        else:
            raise Exception()
        return message
