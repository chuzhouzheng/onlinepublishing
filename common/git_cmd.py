__author__ = 'Administrator'
import os



class Cmd(object):
    def __init__(self, command, cd=None,):
        self.command = command
        self.cd = cd
        
    def exec_cmd(self):
        result = os.popen(self.command)
        return result.read()

