import subprocess


class Node:
    def __init__(self, idx: str, cust: str):
        self._idx = idx
        self._cust = cust
        self._status = True
        self.exec_comm_docker("docker run -d --network graph-network \
                                chsponciano/noderabbit python ServerAppInitialize.py " + idx + " " + cust)

    def start(self):
        if not self._status:
            self.exec_comm_docker("docker start " + self._idx)
            self._status = True

    def stop(self):
        if self._status:
            self.exec_comm_docker("docker stop -t 1 " + self._idx)
            self._status = False

    def exec_comm_docker(self, command):
        with open("output.log", "a") as output:
            subprocess.call(command, shell=True, stdout=output, stderr=output)
