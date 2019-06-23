from ControllerAppSender import ControllerAppSender
from ControllerAppListener import ControllerAppListener
from ControllerAppQueue import ControllerAppQueue
from ControllerAppTaskScheduler import ControllerAppTaskScheduler
from ControllerAppConstants import HEALTHCHECK_INTERVAL
from colorama import init, Fore
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
listener = ControllerAppListener(queue, sender, task_scheduler)

listener.start_listening_async()
task_scheduler.start()

print(f'Controller app initialized.')
