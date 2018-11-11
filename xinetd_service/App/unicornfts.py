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
import pathlib

op_list = ["put", "get", "del", "list"]
port = 8080
host = "localhost"

# Logging environment setup
log = logging.getLogger("client" + __name__)
log.setLevel(logging.DEBUG)

log_fh = logging.FileHandler("client.log")
log_fh.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log_fh.setFormatter(formatter)
log.addHandler(log_fh)

log.info("Init Message")

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def send_message(s_socket, message):
    request_pickle = pickle.dumps(message, pickle.HIGHEST_PROTOCOL)
    log.info("request pickle ready")

    request_pickle += b'\n'

    s_socket.send(request_pickle)
    log.info("request pickle send")

def get_message(s_socket):
    log.debug("get_message function called")
    transmission_check_pickle = []

    s_socket.shutdown(socket.SHUT_WR)

    BUFFER_SIZE = 4096

    while True:
        data = s_socket.recv(BUFFER_SIZE)
        log.debug("Data recieved")
        transmission_check_pickle.append(data)
        if len(data) < BUFFER_SIZE:
            log.debug("Data transmission end")
            break
    
    transmission_check_pickle = b''.join(transmission_check_pickle)

    try:
        transmission_check = pickle.loads(transmission_check_pickle)
    except pickle.UnpicklingError as err:
        log.error("Unpickling Error")
        print("An error occur!", err)
        sys.exit(0)

    s_socket.close()

    return transmission_check

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

    send_message(s_socket, request)
    transmission_check = get_message(s_socket)

    if transmission_check["send"] != "OK":
        log.info(transmission_check["message_log"])
        print(transmission_check["message"])
        sys.exit(0)
    
    log.debug("Starting to read local file")
    with open(sys.argv[2], "rb") as binary_file:
        data = binary_file.read()
    log.debug("local file readed")

    request = {
        "op"        : "put",
        "username"  : getpass.getuser(),
        "filename"  : pathlib.Path(sys.argv[2]).name,
        "md5"       : md5(sys.argv[2]),
        "file"      : data
    }
    
    s_socket = create_socket()
    send_message(s_socket, request)
    
    transmission_check = get_message(s_socket)

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
    
    file_path = pathlib.Path(sys.argv[2])

    # Client has to have the file locally
    if not os.path.isfile(file_path.absolute()):
        log.info("File isn't found locally <Operation Reject>")
        print("File doesn't exist on local")
        sys.exit(0)
    
    request = {
        "op"            : "del",
        "username"      : getpass.getuser(),
        "filename"      : pathlib.Path(sys.argv[2]).name,
        "filesize"      : os.stat(file_path.absolute()).st_size,
        "md5"           : md5(file_path.absolute())
    }

    s_socket = create_socket()
    send_message(s_socket, request)

    server_reply = get_message(s_socket)

    if server_reply["success"] == "yes":
        log.info("Del operation ended successfully")
        print("File", file_path.name, "is deleted")
    else:
        log.warning("Del operation ended with faliure <server message : %s>", server_reply["message_log"])
        print(server_reply["message"])

def list_files():
    log.info("List operation starts")

    s_socket = create_socket()
    request = {
        "op"        : "list",
        "username"  : getpass.getuser()
    }
    
    send_message(s_socket, request)
    
    response = get_message(s_socket)

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