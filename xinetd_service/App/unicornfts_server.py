#!/usr/bin/python

"""
unicornDTS (server side) is a file transfer service on xinetd

"""

import sys
import time

while(1):
        sys.stdout.write("working\n")
        sys.stdout.flush()
        time.sleep(.1)
