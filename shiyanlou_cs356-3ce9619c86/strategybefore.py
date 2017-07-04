# _*_ coding: utf-8 _*_
class Question(object):
    def __init__(self, admin=True):
        self._admin = admin
    def show(self):
        if self._admin is True:
            return "show page with admin"
        else:
            return "show page with user"

if __name__ == '__main__':
    q = Question(admin=False)
    print(q.show())
