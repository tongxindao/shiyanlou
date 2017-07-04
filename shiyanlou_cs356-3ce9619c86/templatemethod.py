# _*_ coding: utf-8 _*_

import abc

class Fishing(object):
    __metaclass__ = abc.ABCMeta
    def finishing(self):
        self.prepare_bait()
        self.go_to_riverbank()
        self.find_location()
        print("start fishing")

    @abc.abstractmethod
    def prepare_bait(self):
        pass

    @abc.abstractmethod
    def go_to_riverbank(self):
        pass

    @abc.abstractmethod
    def find_location(self):
        pass

class JohnFishing(Fishing):
    def prepare_bait(self):
        print("John: buy bait from Taobao")

    def go_to_riverbank(self):
        print("John: to river driving")

    def find_location(self):
        print("John: select location on the island")

class SimonFishing(Fishing):
    def prepare_bait(self):
        print("Simon: buy bait from JD")

    def go_to_riverbank(self):
        print("Simon: to river by biking")

    def find_location(self):
        print("Simon: select location on the island")

if __name__ == '__main__':
    f = JohnFishing()
    f.finishing()

    f = SimonFishing()
    f.finishing()
