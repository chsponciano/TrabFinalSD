from ServerAppSender import ServerAppSender
from ServerAppListener import ServerAppListener
from ServerAppQueue import ServerAppQueue
from ServerAppMapper import ServerAppMapper
from colorama import init, Fore
import sys


init()
args = sys.argv[1:]

assert len(args) is 2

this_queue_name = args[0]
processing_time = args[1]

queue = ServerAppQueue(this_queue_name, processing_time)
mapper = ServerAppMapper(queue)
sender = ServerAppSender(queue)
listener = ServerAppListener(queue, sender, mapper)

listener.start_listening_async()

print(f'Queue initialized with name {this_queue_name} and processing time of {processing_time}.')
