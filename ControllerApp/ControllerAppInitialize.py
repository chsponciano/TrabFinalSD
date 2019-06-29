from ControllerAppSender import ControllerAppSender
from ControllerAppListener import ControllerAppListener
from ControllerAppQueue import ControllerAppQueue
from ControllerAppTaskScheduler import ControllerAppTaskScheduler
# from ControllerAppSocket import ControllerAppSocket
from ControllerAppConstants import HEALTHCHECK_INTERVAL
from ControllerAppAmazon import ControllerAppAmazon
from NodeController import NodeController
from colorama import init, Fore
from ControllerAppFlask import run, add_node_controller, add_sender, add_amazon
import sys


init()

tasks = [
    {
        'interval': HEALTHCHECK_INTERVAL,
        'message': 'healthcheck'
    }
]

queue = ControllerAppQueue()
sender = ControllerAppSender(queue)
task_scheduler = ControllerAppTaskScheduler(sender, tasks)
node_controller = NodeController()
amazon = ControllerAppAmazon()
listener = ControllerAppListener(queue, sender, task_scheduler, node_controller, amazon=amazon)

listener.start_listening_async()
task_scheduler.start()

print(f'Controller app initialized.')

add_node_controller(node_controller)
add_sender(sender)
add_amazon(amazon)
run()
