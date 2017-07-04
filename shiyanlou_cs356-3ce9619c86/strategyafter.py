# _*_ coding: utf-8 _*_

import abc

class AbsShow(object):
    __metaclass__ = abc.ABCMeta
    @abc.abstractmethod
    def show(self):
        pass

class AdminShow(AbsShow):
    def show(self):
        return "show with admin"

class UserShow(AbsShow):
    def show(self):
        return "show with user"

class Question(object):
    def __init__(self, show_obj):
        self.show_obj = show_obj
    def show(self):
        return self.show_obj.show()

if __name__ == '__main__':
    q = Question(show_obj=AdminShow())
    print(q.show())
    q.show_obj = UserShow()
    print(q.show())
