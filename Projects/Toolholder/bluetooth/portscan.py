#!/usr/env/bin python3
# -*-coding:utf-8 -*-

import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

target = input("Please input the website to scan:")

def psan(port):
    try:
        con = sock.connect((target, port))
        return True
    except:
        return False


for port in range(30):
    print("%.2f%%"%(port/30*100))
    if psan(port):
        print("port", port)
