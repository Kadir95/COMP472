#!/usr/bin/python
"""
unicornDTS (client side) is a file transfer service on xinetd

"""

import socket

try:
    server_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("socket successfully created")
except socket.error as err:
    print("socket conneciton failed with error", err)

port = 8181

try:
    server_s.connect(("localhost", port))
except socket.error as err:
    print("server connection failed with error", err)
finally:
    while 1:
        data = server_s.recv(1024)
        print("Rec:", data)