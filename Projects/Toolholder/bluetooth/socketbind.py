#!/usr/bin/env python3
# -*-coding:utf-8 -*-

import socket
import sys

HOST = ""
PORT = 5555

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    sock.bind((HOST, PORT))
    print("Bind successfully!")
except socket.error as msg:
    print("Bind failed. Error code:" + str(msg[0] + "Message" + msg[1]))
    sys.exit()

print("Socket bind complete!")


sock.listen(10)

conn, addr = sock.accept()

print("Connect with" + addr[0] + ":" + str(addr[1]))
