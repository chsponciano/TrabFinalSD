import os


class ControllerAppAmazon(object):
    def __init__(self):
        pass
    
    def new_instance(self, node_name, processing_time):
        os.popen(f'start "cmd" "C:\\Users\\vinic\\Desktop\\TrabFinalSD\\ServerApp\\ServerAppInitialize.py" "{node_name}" "{processing_time}"')