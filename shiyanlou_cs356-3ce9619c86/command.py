# _*_ coding: utf-8 _*_

import abc

class VmReceiver(object):
    def start(self):
        print("Virtual machine start")

    def stop(self):
        print("Virtual machine stop")

class Command(object):
    __metaclass__ = abc.ABCMeta
    @abc.abstractmethod
    def execute(self):
        pass

class StartVmCommand(Command):
    def __init__(self, recevier):
        self.recevier = recevier

    def execute(self):
        self.recevier.start()

class StopVmCommand(Command):
    def __init__(self, recevier):
        self.recevier = recevier

    def execute(self):
        self.recevier.stop()

class ClientInvoker(object):
    def __init__(self, command):
        self.command = command

    def do(self):
        self.command.execute()

if __name__ == '__main__':
    receiver = VmReceiver()
    start_command = StartVmCommand(receiver)

    client = ClientInvoker(start_command)
    client.do()

    stop_command = StopVmCommand(receiver)
    client.command = stop_command
    client.do()
