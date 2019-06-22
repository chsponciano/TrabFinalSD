from pika import BlockingConnection, ConnectionParameters


connection = BlockingConnection(ConnectionParameters('localhost'))
channel = connection.channel()
qd_content = channel.queue_declare(queue="q1",passive=True)

channel.close()

print(qd_content)

