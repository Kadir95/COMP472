#!/usr/bin/python
"""
unicornDTS (server side) is a file transfer service on xinetd

"""

import sys
import time
import logging
import pickle
import os 
import hashlib
import subprocess
import pathlib

path="/home/mzp7/workspace/comp472/xinetd_service/data/"

# Logging environment setup
log = logging.getLogger("server" + __name__)
log.setLevel(logging.DEBUG)

log_fh = logging.FileHandler("/home/mzp7/workspace/comp472/xinetd_service/" + "server.log")
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

def put(data):
        pass

def put_check(data):
        log.debug("put_check username: " + data["username"])
        if not os.path.isdir(path + data["username"]):
                log.debug("put_check username: " + data["username"] + "there is no directory")
                reply = {
                        "send"          : "NOT",
                        "message"       : "User dictinoary is not created",
                        "message_log"   : "User dictinoary is not created"
                }
                reply_pickle = pickle.dumps(reply, pickle.HIGHEST_PROTOCOL)
                sys.stdout.buffer.write(reply_pickle)
                sys.stdout.flush()
                return
        
        user_path = path + data["username"] + "/"

        if os.path.isfile(user_path + data["filename"]):
                if data["md5"] == md5(user_path + data["filename"]):
                        log.debug("put_check username: " + data["username"] + " the file already exists")
                        reply = {
                                "send"          : "NOT",
                                "message"       : "The file already exists",
                                "message_log"   : "The file already exists"
                        }
                        reply_pickle = pickle.dumps(reply, pickle.HIGHEST_PROTOCOL)
                        sys.stdout.buffer.write(reply_pickle)
                        sys.stdout.flush()
                        return
        
        log.debug("put_check username: " + data["username"] + " send a request for the file")
        reply = {
                "send"          : "OK",
                "message"       : "send a request for the file",
                "message_log"   : "send a request for the file"
        }
        reply_pickle = pickle.dumps(reply, pickle.HIGHEST_PROTOCOL)
        sys.stdout.buffer.write(reply_pickle)
        sys.stdout.flush()
        
def get(data):
        pass

def delete(data):
        pass

def list_files(data):
        log.info("list file function started")

        user_path = path + data["username"] + "/"
        if not os.path.exists(user_path):
                log.info("User directory created <user: " + data["username"] + ">")
                os.makedirs(user_path)

                response = {
                        "success"       : "yes",
                        "message"       : "New directory is created (" + data["username"] + ")",
                        "message_log"   : "New directory is created (" + data["username"] + ")"
                }

                response_pickle = pickle.dumps(response, pickle.HIGHEST_PROTOCOL)
                sys.stdout.buffer.write(response_pickle)
                sys.stdout.flush()
                log.debug("List function send creation message to client")
                return
        if os.path.isdir(user_path):
                log.info("user directory found <user: " + data["username"] + ">")
                output = subprocess.check_output(["ls", "-l", user_path]).decode()
                log.debug("List function list the directory \n" + str(output))
                response = {
                        "success"       : "yes",
                        "message"       : output,
                        "message_log"   : "Directory is listed"
                }
                response_pickle = pickle.dumps(response, pickle.HIGHEST_PROTOCOL)
                sys.stdout.buffer.write(response_pickle)
                sys.stdout.flush()
                log.debug("List function ended successfully")
                return
        
        log.error("List function couldn't figure out the directory")
        response = {
                "success"       : "no",
                "message"       : "err list",
                "message_log"   : "err list"
        }
        response_pickle = pickle.dumps(response, pickle.HIGHEST_PROTOCOL)
        sys.stdout.buffer.write(response_pickle)
        sys.stdout.flush()
        log.error("List function send the error message to client")
        return


data_pickle  = sys.stdin.buffer.read()

data = pickle.loads(data_pickle)

opetaion = data["op"]

log.debug("Received operation is " + opetaion)

if not os.path.exists(path):
        os.makedirs(path)

if opetaion == "put":
        log.debug("Put operation starts")
        put(data)
        
if opetaion == "put_check":
        log.debug("Put_check operation starts")
        put_check(data)

if opetaion == "get":
        log.debug("Get operation starts")
        get(data)
        
if opetaion == "del":
        log.debug("Del operation starts")
        delete(data)

if opetaion == "list":
        log.debug("List operation starts")
        list_files(data)