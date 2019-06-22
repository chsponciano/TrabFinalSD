from ControllerAppSender import ControllerAppSender
from ControllerAppListener import ControllerAppListener
from ControllerAppQueue import ControllerAppQueue
from colorama import init, Fore
import sys


init()

queue = ControllerAppQueue()
sender = ControllerAppSender(queue)
listener = ControllerAppListener(queue, sender)

listener.start_listening_async()

print(f'Controller app initialized.')
