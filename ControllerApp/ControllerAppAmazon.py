import subprocess

class ControllerAppAmazon(object):
    
    def new_instance(self, node_name, processing_time):
        self.exec_command("docker run -d --name " + str(node_name) + " --network graph-network --hostname " + str(node_name) + " \
                                chsponciano/noderabbit python ServerAppInitialize.py " + str(node_name) + " " + str(processing_time))
    
    def delete_instance(self, node_name):
        self.exec_command("docker rm -f " + node_name)

    def exec_command(self, command):
        with open("output.log", "a") as output:
            subprocess.call(command, shell=True, stdout=output, stderr=output)