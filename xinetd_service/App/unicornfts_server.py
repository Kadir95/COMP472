#!/usr/bin/python
"""
unicornDTS (server side) is a file transfer service on xinetd

"""

import sys
import time
import logging
import pickle

log = logging.getLogger("server" + __name__)
log.setLevel(logging.NOTSET)

log_fh = logging.FileHandler("server.log")
log_fh.setLevel(logging.NOTSET)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log_fh.setFormatter(formatter)
log.addHandler(log_fh)

def put(data):
        pass

def put_check(data):
        pass

def get(data):
        pass

def delete(data):
        pass

def list_files(data):
        pass

data_pickle  = sys.stdin.readline().strip()

data = pickle.loads(data_pickle)

opetaion = data["op"]

log.debug("Received operation is ")

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

sys.stdout.flush()