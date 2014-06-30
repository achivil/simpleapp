# -*- coding: utf-8 -*-
#
#for guard nids server

import os
import re
import time
from subprocess import Popen, PIPE

def watcher():
    """
    """
    cmd = "ps ax | grep 'resourceupload.py' | grep -v 'grep' "
    ru_pid = os.popen(cmd).readlines()
    cmd = "ps ax | grep '/host/graud.py' | grep -v 'grep' "
    graud_pid = os.popen(cmd).readlines()
    cmd = "ps ax | grep 'uwsgi -x' | grep -v 'grep' "
    uwsgi_pid = os.popen(cmd).readlines()
    #print ru_pid, graud_pid, uwsgi_pid
    if not ru_pid:
        cmd = "python resourceupload.py"
        res = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE, close_fds=True)
    else:
        print "resourceupload is running"
    if not graud_pid:
        cmd = "python ../host/graud.py"
        res = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE, close_fds=True)
    else:
        print "host is running"
    if not ru_pid:
        cmd = "uwsgi -x test_nids.xml --ignore-sigpipe --ignore-write-errors --daemonize uwsgi.log&"
        res = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE, close_fds=True)
    else:
        print "uwsgi is running"

def main():
    while 1:
        time.sleep(2)
        watcher()

if __name__ == "__main__":
    main()

