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
import json

with open(os.environ["SERVERSETTINGS"], "r") as setting_file:
        settings = json.load(setting_file)

path = settings["server"]["data_path"]

# Logging environment setup
log = logging.getLogger("server" + __name__)
log.setLevel(logging.DEBUG)

if not os.path.isdir(settings["server"]["logging_path"]):
        os.makedirs(settings["server"]["logging_path"])

log_fh = logging.FileHandler(settings["server"]["logging_path"] + "server.log")
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

def put(data):
        log.info("Put operation starts")

        user_path = path + data["username"] + "/"
        file_path = user_path+ data["filename"]

        log.debug("data size : " + str(len(data["file"])/1024))
        with open(file_path, "wb") as file:
                file.write(data["file"])
                file.close()
        log.debug("Data is written to %s", file_path)

        if md5(file_path) != data["md5"]:
                log.info("MD5 check failed")
                os.remove(file_path)
                reply = {
                        "success"       : "no",
                        "message"       : "MD5s didn't match",
                        "message_log"   : "MD5s didn't match"
                }
                send_message(reply)
                return

        log.info("File is transferred successfully")

        reply = {
                "success"       : "yes",
                "message"       : "File is transferred successfully",
                "message_log"   : "File is transferred successfully"
        }
        send_message(reply)
        
def put_check(data):
        log.debug("Put_check operation starts <username:%s>", data["username"])

        user_path = path + data["username"] + "/"
        file_path = user_path + data["filename"]

        if not os.path.isdir(user_path):
                log.debug("put_check <username:%s> there is no directory", data["username"])
                reply = {
                        "send"          : "NOT",
                        "message"       : "There is no user directory",
                        "message_log"   : "There is no user directory"
                }
                send_message(reply)
                return
        
        if os.path.isfile(file_path):
                if data["md5"] == md5(file_path):
                        log.debug("put_check <username:%s> the file already exists", data["username"])
                        reply = {
                                "send"          : "NOT",
                                "message"       : "The file already exists",
                                "message_log"   : "The file already exists"
                        }
                        send_message(reply)
                        return
        
        log.debug("put_check <username:%s> send a request for the file", data["username"])
        reply = {
                "send"          : "OK",
                "message"       : "send a request for the file",
                "message_log"   : "send a request for the file"
        }
        send_message(reply)
        
def get(data):
        log.info("Get operation starts")

        user_path = path + data["username"] + "/"
        file_path = user_path + data["filename"]

        log.debug("File path : %s", file_path)

        if not os.path.isfile(file_path):
                log.info("File doesn't found")
                reply = {
                        "success"       : "no",
                        "message_log"   : "File doesn't found",
                        "message"       : "File doesn't found"
                }
                send_message(reply)
                return
        
        with open(file_path, "rb") as file:
                reply = {
                        "success"       : "yes",
                        "message_log"   : "File is found",
                        "message"       : "File is found",
                        "filename"      : file_path.split("/")[-1],
                        "file"          : file.read(),
                        "md5"           : md5(file_path)
                }
                send_message(reply)

def delete(data):
        log.info("Del operation starts")
        
        user_path = path + data["username"] + "/"
        file_path = user_path + data["filename"]
        log.debug("File path : %s", file_path)

        if not os.path.isfile(file_path):
                log.info("File doesn't exists")
                reply = {
                        "success"       : "no",
                        "message_log"   : "File doesn't found",
                        "message"       : file_path.split("/")[-1] + " doesn't found"
                }
                send_message(reply)
                return
        
        if data["filesize"] != os.stat(file_path).st_size:
                log.info("File sizes doesn't match")
                reply = {
                        "success"       : "no",
                        "message_log"   : "File sizes don't match",
                        "message"       : file_path.split("/")[-1] + " sizes don't match"
                }
                send_message(reply)
                return

        if md5(file_path) != data["md5"]:
                log.info("MD5 check failed")
                reply = {
                        "success"       : "no",
                        "message_log"   : "MD5 check failed",
                        "message"       : file_path.split("/")[-1] + " MD5 check failed"
                }
                send_message(reply)
                return

        os.remove(file_path)
        log.info("File is deleted successfully")
        reply = {
                "success"       : "yes",
                "message_log"   : "File is deleted successfully",
                "message"       : file_path.split("/")[-1] + " is deleted successfully"
        }
        send_message(reply)
        log.info("Message is send")

def list_files(data):
        log.info("list file operation started")

        user_path = path + data["username"] + "/"

        if not os.path.exists(user_path):
                log.info("User directory created <username:%s>", data["username"])
                os.makedirs(user_path)

                response = {
                        "success"       : "yes",
                        "message"       : "New directory is created (" + data["username"] + ")",
                        "message_log"   : "New directory is created (" + data["username"] + ")"
                }
                send_message(response)
                log.debug("List function send the directory creation message to the client")
                return
        
        if os.path.isdir(user_path):
                log.info("user directory found <username:%s>", data["username"])
                output = subprocess.check_output(["ls", "-l", user_path]).decode()

                if "total 0" in output:
                        output = "There is no stored file"

                log.debug("List function list the directory \n%s", str(output))
                response = {
                        "success"       : "yes",
                        "message"       : output,
                        "message_log"   : "Directory is listed"
                }
                send_message(response)
                log.debug("List function is ended successfully")
                return
        
        log.error("List function couldn't figure out the directory")
        response = {
                "success"       : "no",
                "message"       : "List function couldn't figure out the directory",
                "message_log"   : "List function couldn't figure out the directory"
        }
        send_message(response)
        log.error("List function send the error message to the client")

data_pickle  = sys.stdin.buffer.read()

data = pickle.loads(data_pickle)

operation = data["op"]

log.debug("Received operation is " + operation)

if not os.path.exists(path):
        os.makedirs(path)

if operation == "put":
        log.debug("Put operation is called")
        put(data)
        
if operation == "put_check":
        log.debug("Put_check operation is called")
        put_check(data)

if operation == "get":
        log.debug("Get operation is called")
        get(data)
        
if operation == "del":
        log.debug("Del operation is called")
        delete(data)

if operation == "list":
        log.debug("List operation is called")
        list_files(data)