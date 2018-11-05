"""
unicornDTS (server side) is a file transfer service on xinetd

"""
#!/usr/bin/python

import sys
import time

while(1):
        sys.stdout.write("working - " + sys.stdin.readline() + "\n") 
        sys.stdout.flush()
