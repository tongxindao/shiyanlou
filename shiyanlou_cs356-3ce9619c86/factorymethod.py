# _*_ coding: utf-8 _*_
import random
import abc
class BasicCourse(object):
    """基础课程"""
    def get_labs(self):
        return "basic_course: labs"
    def __str__(self):
        return "BasicCourse"

class ProjectCourse(object):
    """项目课"""
    def get_labs(self):
        return "project_course: labs"
    def __str__(self):
        return "ProjectCourse"

class Factory(object):
    """抽象工厂类"""
    __metaclass__ = abc.ABCMeta
    @abc.abstractmethod
    def create_course(self):
        pass

class BasicCourseFactory(object):
    """基础课程工厂类"""
    def create_course(type):
        return BasicCourse()

class ProjectCourseFactory(object):
    """项目课程工厂类"""
    def create_course(type):
        return ProjectCourse()

def get_factory():
    """随机获取一个工厂类"""
    return random.choice([BasicCourseFactory, ProjectCourseFactory])()

if __name__ == '__main__':
    factory = get_factory()
    course = factory.create_course()
    print(course.get_labs())
