#_*_ coding:utf-8 _*_
# file name:my_socket.py

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scatter import Scatter
from kivy.uix.carousel import Carousel
from kivy.uix.button import Button
import math
from socket import *
from Queue import Queue
import threading
import kivy.clock
import time
from time import ctime
import struct
import re

my_socket_queue = Queue(10240)
my_flag_queue = Queue(10)
HOST = '192.168.42.4'
PORT = 21500
BUFSIZ = 10240
# ADDR = (HOST, PORT)
# tcpCliSock = socket(AF_INET, SOCK_STREAM)
flag = []
my_flag = 0

def writeUTF(s):
    s = s.encode('utf')
    ss = struct.pack('>H%ds' % len(s), len(s), s)
    return ss

def readUTF(s):
    s = s.decode('utf8')
    return s[2:]

def writeQ(queue, data):
    # print 'producing object for Q...'
    queue.put(data, 1)
    # print 'size now', queue.qsize()

def readQ(queue):
    val = queue.get(1)
    return val

class MyThread(threading.Thread):
    def __init__(self, func, args, name = ''):
        threading.Thread.__init__(self)
        self.name = name
        self.func = func
        self.args = args

    def getResult(self):
        return self.res

    def run(self):
        print 'starting', self.name, 'at:', ctime()
        self.res = apply(self.func, self.args)
        print self.name, 'finished at:', ctime()

def socket_read(socket_c, str_array, queue):
    while my_flag_queue.qsize():
        try:
            print 'waiting data...'
            data = socket_c.recv(BUFSIZ)
        except IOError,e:
            print 'read data cause an IOError!'
            break
        if not data:
            break
            # print data
            # writeQ(queue, data)
        cmd = []
        cmd = re.split('\n', data, 0)
        print 'cmd is:', cmd
        for cmd_data in cmd:
            print cmd_data
            if cmd_data:
                string_format = readUTF(cmd_data)
                print 'string format is:', string_format
                writeQ(queue, string_format)
    print 'finished!'
    socket_c.close()

class myCarousel(Carousel):
    pass

class my_socketApp(App):
    def my_callback(self, dt):
        # print 'I am alive...'
        if my_socket_queue.qsize():
            my_str = readQ(my_socket_queue)
            print 'my_str is %s\n' % my_str
            if my_str:
                self.root.text_input7.text += my_str + '\n'

    def connect_server(self):
        HOST = self.root.text_input5.text
        ADDR = (HOST, PORT)
        if self.root.connect.text == 'Connect':
            try:
                tcpCliSock = socket(AF_INET, SOCK_STREAM)
                tcpCliSock.connect(ADDR)
                # tcpCliSock.setblocking(False)
                print len(flag)
                flag.append(1)
                my_flag = 1
                kivy.clock.Clock.schedule_interval(self.my_callback, 0.1)
                self.root.connect.text = 'Disconnect'
                print 'connected!'
                print len(flag)
            except Exception as e:
                print e
                return
        else:
            try:
                flag.pop()
                my_flag = 0
                self.root.connect.text = 'Connect'
                print len(flag)
            except Exception as e1:
                print e1
        global my_flag
        if my_flag == 1:
            writeQ(my_flag_queue, 'flag')
            socket_read_thread = MyThread(socket_read, (tcpCliSock, my_flag_queue, my_socket_queue), socket_read.__name__)
            socket_read_thread.start()
        else:
            my_str = readQ(my_flag_queue)
            print my_str
            # socket_read_thread.join()
            try:
                tcpCliSocket.send(writeUTF(u"%s" % (u'closed')))
            except Exception as e:
                pass
            global tcpCliSock
            # tcpCliSock.close()
            print 'disconnected!'

    def send(self):
        try:
            tcpCliSock.send(writeUTF(u"%s" % (self.root.text_input6.text)))
        except Exception as e:
            pass
        print 'send over!'

if __name__ == '__main__':
    my_socketApp().run()
