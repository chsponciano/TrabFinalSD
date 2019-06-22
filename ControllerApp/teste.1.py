from pika import BlockingConnection, ConnectionParameters
from json import dumps


connection = BlockingConnection(ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue="teste-controller")
channel.basic_consume(
        queue='teste-controller',
        on_message_callback=lambda ch, method, properties, body: print(f'Recebeu {body}'),
        auto_ack=True
)

channel.start_consuming()

channel.close()


