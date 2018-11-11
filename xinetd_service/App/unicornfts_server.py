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

def send_message(message):
        reply_pickle = pickle.dumps(message, pickle.HIGHEST_PROTOCOL)
        sys.stdout.buffer.write(reply_pickle)
        sys.stdout.flush()

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def md5v(data):
        hash = hashlib.md5()
        hash.update(data)
        return hash.hexdigest()

def put(data):
        log.info("put function starts")
        user_path = path + data["username"] + "/"
        file_path = user_path + data["filename"]

        log.debug("data size : " + str(len(data["file"])/1024))
        with open(file_path, "wb") as file:
                file.write(data["file"])
                file.close()
        
        if md5(file_path) != data["md5"]:
                log.info("files md5 doesn't mach")
                os.remove(user_path + data["filename"])
                reply = {
                        "success"       : "no",
                        "message"       : "MD5s didn't mach",
                        "message_log"   : "MD5s didn't mach"
                }
                reply_pickle = pickle.dumps(reply, pickle.HIGHEST_PROTOCOL)
                sys.stdout.buffer.write(reply_pickle)
                sys.stdout.flush()
                return

        log.info("file write")

        reply = {
                "success"       : "yes",
                "message"       : "File successfully trasfered",
                "message_log"   : "File successfully trasfered"
        }
        reply_pickle = pickle.dumps(reply, pickle.HIGHEST_PROTOCOL)
        sys.stdout.buffer.write(reply_pickle)
        sys.stdout.flush()
        return
        
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
        return
        
def get(data):
        pass

def delete(data):
        log.info("Del oprateion starts")
        
        user_path = pathlib.Path(path + data["username"] + "/")
        file_path = pathlib.Path(user_path + data["filename"])  
        log.debug("File path : %s", file_path.absolute())

        if not os.path.isfile(file_path.absolute()):
                log.info("File doesn't exists")
                reply = {
                        "success"       : "no",
                        "message_log"   : "File couldn't find",
                        "message"       : file_path.name + " couldn't find"
                }
                send_message(reply)
                return
        
        if data["filesize"] != os.stat(file_path.absolute()).st_size:
                log.info("File sizes doesn't match")
                reply = {
                        "success"       : "no",
                        "message_log"   : "File sizes don't mach",
                        "message"       : file_path.name + " sizes don't mach"
                }
                send_message(reply)
                return

        if md5(file_path.absolute()) != data["md5"]:
                log.info("File md5s doesn't match")
                reply = {
                        "success"       : "no",
                        "message_log"   : "File md5s don't mach",
                        "message"       : file_path.name + " md5s don't mach"
                }
                send_message(reply)
                return

        os.remove(file_path.absolute())
        log.info("File is deleted successfully")
        reply = {
                "success"       : "yes",
                "message_log"   : "File deleted succesfully",
                "message"       : file_path.name + " deleted succesfully"
        }
        send_message(reply)
        log.info("Message is send")

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