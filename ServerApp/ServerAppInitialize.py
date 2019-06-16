from ServerAppSender import ServerAppSender
from ServerAppListener import ServerAppListener
from ServerAppQueue import ServerAppQueue
from ServerAppMapper import ServerAppMapper
import sys

args = sys.argv

if len(args) < 2:
    raise Exception()

this_queue_name = args[1]
queues_to_connect = set(args[2:])

mapper = ServerAppMapper()
queue = ServerAppQueue(this_queue_name)
sender = ServerAppSender(queue)
listener = ServerAppListener(queue, sender, mapper)

listener.start_listening_async()

for queue in queues_to_connect:
    sender.send_message_to(
        {
            'message': 'first_connect', 
            'args': {
                'sender_queue_name': this_queue_name
            }
        }, 
        queue
    )

print(f'Queue initialized with name {this_queue_name}.')