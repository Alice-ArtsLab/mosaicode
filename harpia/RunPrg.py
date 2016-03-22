import  os 

from threading import Thread

class RunPrg(Thread):
    def __init__(self, cmd):
        Thread.__init__(self)
        self.cmd = cmd

    def run(self):
        os.system(self.cmd + " 2> RunErrorLog")

