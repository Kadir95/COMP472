#!/usr/bin/python
"""
unicornDTS (client side) is a file transfer service on xinetd

"""

import socket
import time
import sys
import logging
import pickle
import os
import getpass
import hashlib

op_list = ["put", "get", "del", "list"]
port = 8080
host = "localhost"

log = logging.getLogger("client" + __name__)
log.setLevel(logging.NOTSET)

log_fh = logging.FileHandler("client.log")
log_fh.setLevel(logging.NOTSET)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log_fh.setFormatter(formatter)
log.addHandler(log_fh)

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def create_socket():
    try:
        server_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        log.debug("socket successfully created")
    except socket.error as err:
        log.error("socket conneciton failed with error" + err)

    try:
        server_s.connect((host, port))
        log.debug("socket successfully connected")
        return server_s
    except socket.error as err:
        log.error("server connection failed with error" + err)
    log.error("socket failed")
    return None

def put():
    log.info("Put operation starts")
    
    if len(sys.argv) < 3:
        log.warning("User arguments insufficient")
        print("Usage: " + sys.argv[0] + " put <file name>")
        sys.exit(0)
    
    if not os.path.isfile(sys.argv[2]):
        log.warning("User argument is not a file")
        print("Usage: " + sys.argv[0] + " put <file name>")
        sys.exit(0)
    
    s_socket = create_socket()

    request = {
        "op"        : "put_check",
        "username"  : getpass.getuser(),
        "filename"  : os.path.splitext(sys.argv[2])[0],
        "md5"       : md5(sys.argv[2])
    }

    request_pickle = pickle.dumps(request, pickle.HIGHEST_PROTOCOL)
    log.info("put_check request pickle ready")

    s_socket.send(request_pickle)
    log.info("put_check request pickle send")

    transmission_check_pickle = b""
    while True:
        data = s_socket.recv(4096)
        if not data:
            break
        transmission_check_pickle += data
    print(transmission_check_pickle)
    try:
        transmission_check = pickle.loads(transmission_check_pickle)
    except pickle.UnpicklingError as err:
        log.error("Unpickling Error")
        print("An error occur!", err)
        sys.exit(0)

    if transmission_check["send"] != "OK":
        log.info(transmission_check["message_log"])
        print(transmission_check["message"])
        sys.exit(0)
    
    with open(sys.argv[2], "rb") as binary_file:
        data = binary_file.read()

    request = {
        "op"        : "put",
        "username"  : getpass.getuser(),
        "filename"  : os.path.splitext(sys.argv[2])[0],
        "md5"       : md5(sys.argv[2]),
        "file"      : data
    }
    
    request_pickle = pickle.dumps(request, pickle.HIGHEST_PROTOCOL)
    s_socket.send(request_pickle)

    transmission_check_pickle = s_socket.recv(4096)
    try:
        transmission_check = pickle.loads(transmission_check_pickle)
    except pickle.UnpicklingError as err:
        log.error("Unpickling Error at " + err)
        print("An error occur!")
        sys.exit(0)
    
    if transmission_check["success"] == "yes":
        log.info("data transfer complete successfully")
        print(transmission_check["message"])
    else:
        log.error("data transfer complete with error")
        print(transmission_check["message"])

def get():
    log.info("Get operation starts")
    s_socket = create_socket()
    s_socket.send(str.encode("get\n"))

    data = s_socket.recv(1024).decode()
    print("Rec:", data)
    pass

def delete():
    log.info("Del operation starts")
    s_socket = create_socket()
    s_socket.send(str.encode("del\n"))

    data = s_socket.recv(1024).decode()
    print("Rec:", data)
    pass

def list_files():
    log.info("List operation starts")

    request = {
        "op"        : "list",
        "username"  : getpass.getuser()
    }
    request_pickle = pickle.dumps(request, pickle.HIGHEST_PROTOCOL)

    s_socket = create_socket()
    s_socket.send(request_pickle)


    response_pickle = b''
    while True:
        data = s_socket.recv(4096)
        if not data:
            break
        response_pickle += data
    
    response = pickle.loads(request_pickle)

    if response["success"] == "yes":
        log.debug(response["message_log"])
        print(response["message"])
    else:
        log.error(response["message_log"])
        print(response["message"])

if len(sys.argv) > 1 and sys.argv[1].lower() in op_list:
    operation = sys.argv[1].lower()
    log.info("User give argumen " + sys.argv[1] + " <" + operation + ">")

    op_num = op_list.index(operation)

    if op_num == 0:
        put()
    if op_num == 1:
        get()
    if op_num == 2:
        delete()
    if op_num == 3:
        list_files()

else:
    print("Usage: " + sys.argv[0] + " <operation>")
    sys.exit(0)





"""
finally:
    while 1:
        sent = input("sent:") + "\n"
        server_s.send(str.encode(sent))
        data = server_s.recv(1024).decode()
        print("Rec:", data)
"""