from ServerAppSender import ServerAppSender
from ServerAppListener import ServerAppListener
from ServerAppQueue import ServerAppQueue
from ServerAppMapper import ServerAppMapper
from colorama import init, Fore
import sys


init()
args = sys.argv

if len(args) != 2:
    raise Exception()

this_queue_name = args[1]

mapper = ServerAppMapper()
queue = ServerAppQueue(this_queue_name)
sender = ServerAppSender(queue)
listener = ServerAppListener(queue, sender, mapper)

listener.start_listening_async()

print(f'Queue initialized with name {this_queue_name}.')
