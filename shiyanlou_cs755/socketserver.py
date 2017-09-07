#!/usr/bin/python
#_*_ coding: utf-8 _*_
# file name: socketserver.py

import socket
from socket import *
import sys
from time import ctime, sleep
import thread
import struct

flag = []
HOST = ''
PORT = 21500
BUFSIZ = 1024
ADDR = (HOST, PORT)
tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.bind(ADDR)
tcpSerSock.listen(5)
str_temp = """hello world~"""

def writeUTF(s):
    s = s.encode('utf')
    ss = struct.pack('>H%ds' % len(s), len(s), s)
    return ss

if True:
    while True:
        print 'waiting for connection...'
        tcpCliSock, addr = tcpSerSock.accept()
        print '...connected from:', addr
        # flag[0] = 1
        tcpCliSock.send(writeUTF(u"%s" % (str_temp + '\n')))
        while True:
            data = tcpCliSock.recv(BUFSIZ)
            if not data:
                break
            print data
            tcpCliSock.send((unicode(data)))
        tcpCliSock.close()
    tcpSerSock.close()
