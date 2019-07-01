import subprocess
import os

class ControllerAppAmazon(object):
    
    def new_instance(self, node_name, processing_time):
        os.popen(f'start "cmd" "C:\\Users\\vinic\\Desktop\\TrabFinalSD\\ServerApp\\ServerAppInitialize.py" "{node_name}" "{processing_time}"')
        # self.exec_command("docker run -d --name " + str(node_name) + " --network graph-network --hostname " + str(node_name) + " \
        #                         chsponciano/noderabbit python ServerAppInitialize.py " + str(node_name) + " " + str(processing_time))
    
    def delete_instance(self, node_name):
        pass
        # self.exec_command("docker rm -f " + str(node_name))

    def start_instance(self, node_name):
        pass
        # self.exec_command("docker start " + str(node_name))

    def exec_command(self, command):
        pass
        # with open("output.log", "a") as output:
        #     subprocess.call(command, shell=True, stdout=output, stderr=output)