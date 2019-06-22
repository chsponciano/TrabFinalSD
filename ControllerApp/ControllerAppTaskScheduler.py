from ControllerAppSender import ControllerAppSender
from ControllerAppConstants import CONTROLLER_QUEUE
from threading import Thread
from time import sleep


class ControllerAppTaskScheduler(object):
    def __init__(self, sender: ControllerAppSender, tasks: list=[]):
        self.sender = sender
        for task in tasks:
            thread = Thread(target=lambda: self.task_scheduled(interval=task['interval'], message=task['message']))
            thread.start()

    def task_scheduled(self, interval: int, message: str):
        while True:
            sleep(interval)
            print(f'Scheduler for {message} running. Time interval is {interval} seconds.')
            self.sender.send_message_to(to=CONTROLLER_QUEUE, message=message)

