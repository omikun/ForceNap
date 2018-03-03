#!/usr/bin/python                                                                                            

''' This script automatically finds PIDs for Unity (or some other app) 
    and suspend those processes whenever desired app  is not in focus. 
    This script is meant to stay running and polls window focus every 1 second
    On receiving keyboard interrupt, will resume
'''
from datetime import datetime
from time import sleep
import sys
import subprocess

def get_pid(name):
    result = subprocess.check_output(['pgrep Unity'], shell=True)
    return result.strip().split('\n')

# if script invoked with an argument, use that as the pid
desiredApp = 'Unity'
if len(sys.argv) > 1:
    desiredApp  = [sys.argv[1]]
else:  # otherwise go find all pids associated with Unity
    pids = get_pid(desiredApp)

print "monitoring Unity, with PIDs:", pids, 
try:
    from AppKit import NSWorkspace
except ImportError:
    print "Can't import AppKit -- maybe you're running python from brew?"
    print "Try running with Apple's /usr/bin/python instead."
    exit(1)

try:
    last_active_app = None
    stop = True
    while True:
        active_app = NSWorkspace.sharedWorkspace().activeApplication()
        if last_active_app != active_app['NSApplicationName']:
            last_active_app = active_app['NSApplicationName']
            print "currently focused on", last_active_app
            if last_active_app == 'Unity':
                print "continuing Unity"
                stop = True
                for pid in pids:
                    subprocess.Popen("kill -CONT " + pid, shell=True)
            elif stop:
                stop = False
                print "stopping unity"
                for pid in pids:
                    subprocess.Popen("kill -STOP " + pid, shell=True)
        sleep(1)
except KeyboardInterrupt:
    print '\nresuming Unity, exiting script'
    for pid in pids:
        subprocess.Popen("kill -CONT " + pid, shell=True)
    sys.exit()
