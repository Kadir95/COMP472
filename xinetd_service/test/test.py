#!/usr/bin/python

import logging
import os
import sys
import time

log = logging.getLogger("server" + __name__)
log.setLevel(logging.DEBUG)

log_fh = logging.FileHandler("/home/mzp7/workspace/comp472/xinetd_service/" + "test.log")
log_fh.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log_fh.setFormatter(formatter)
log.addHandler(log_fh)

log.debug("Init Message")

import subprocess

result = subprocess.check_output(["ls", "-l"])
result = result.decode()
print(type(result))
print(result)

if not b'':
    sys.stdout.buffer.write(b'kadir\n')
    sys.stdout.buffer.flush()
    time.sleep(2)