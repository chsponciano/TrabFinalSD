from ControllerAppSender import ControllerAppSender
from ControllerAppConstants import CONTROLLER_QUEUE, SUPPRESS_LOG_TASK
from threading import Thread
from time import sleep


class ControllerAppTaskScheduler(object):
    def __init__(self, sender: ControllerAppSender, tasks: list=[]):
        self.sender = sender
        self.is_not_shut_down = True
        self.tasks = tasks

    def start(self):
        for task in self.tasks:
            thread = Thread(target=lambda: self.task_scheduled(interval=task['interval'], message=task['message']))
            thread.start()

    def task_scheduled(self, interval: int, message: str):
        while self.is_not_shut_down:
            if not message in SUPPRESS_LOG_TASK:
                print(f'Scheduler for {message} running. Time interval is {interval} seconds.')
            self.sender.send_message_to(to=CONTROLLER_QUEUE, message=message)
            sleep(interval)
    
    def shut_down(self):
        self.is_not_shut_down = False

