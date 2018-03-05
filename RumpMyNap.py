#!/usr/bin/python

from __future__ import print_function
import time
import sys
import subprocess
import os
import signal
import rumps
import logging
from threading import Thread

try:
  from AppKit import NSWorkspace
except ImportError:
  print("Can't import AppKit -- maybe you're running python from brew?")
  print("Try running with Apple's /usr/bin/python instead.")
  sys.exit(1)

SUSPENDED = set()  #set of PIDs that has been suspended
DONT_SUSPEND_NAME = ('Terminal', 'Activity Monitor') #set of apps to never suspend/resume

launchedApps  = NSWorkspace.sharedWorkspace().launchedApplications()
appNames = [ app['NSApplicationName'] for app in launchedApps ]
print(appNames)
desiredApps = set()
teststring = "hello world"

def name_of(app):
    if app is None:
        return None
    app_name = app['NSApplicationName']
    if sys.version_info.major < 3 and isinstance(app_name, unicode):
        # TODO handle errors instead of ignoring them
        app_name = app_name.encode("utf8", "ignore")
    return app_name

rumpsClass = \
'''class AwesomeStatusBarApp(rumps.App):
'''
menuItemString =\
'''    @rumps.clicked(%s)
    def onoff%d(self, sender):
        sender.state = not sender.state
        print(%s)
        if sender.state:
            desiredApps.add(%s)
'''
quit_menu =\
'''    @rumps.clicked('my quit')
    def myquit(self, sender):
        print(\'my own quiting\')
        for pid in SUSPENDED:
            os.kill(int(pid), signal.SIGCONT)
        rumps.quit_application()
'''
for i, launchedApp in enumerate(launchedApps):
    if name_of(launchedApp) in DONT_SUSPEND_NAME:
        continue
    appStr = 'launchedApp[%d]' % i
    appNameStr = '\'%s\'' % name_of(launchedApp)
    rumpsClass += menuItemString % (appNameStr, i, appNameStr, appStr)

rumpsClass += quit_menu
#print(rumpsClass)
exec(rumpsClass)

def start_bar():
    AwesomeStatusBarApp("NMA").run()
    for pid in SUSPENDED:
        os.kill(int(pid), signal.SIGCONT)

def get_pids(app):
    """Returns list of all process IDs for given application."""
    if not app:
        return []
    pid = app['NSApplicationProcessIdentifier']
    pids = [pid]
    try:
        pids += map(int, subprocess.check_output(['pgrep', '-P %s' % pid]).split())
    except subprocess.CalledProcessError:
        pass
    return pids

def otherThread():
    prev_app = None
    while True:
        app = NSWorkspace.sharedWorkspace().activeApplication()
        if prev_app != app:
            print(app['NSApplicationName'])
            if app['NSApplicationName'] == 'Messages':
                print("Continuing ", app['NSApplicationName'])
                pids = get_pids(app)
                for pid in pids:
                    os.kill(int(pid), signal.SIGCONT)
                for pid in pids:
                    os.kill(int(pid), signal.SIGCONT)
            if prev_app and prev_app['NSApplicationName'] == 'Messages':
                print("Stopping ", prev_app['NSApplicationName'])
                pids = get_pids(prev_app)
                for pid in pids:
                    SUSPENDED.add(pid)
                    os.kill(int(pid), signal.SIGSTOP)
            prev_app = app
        time.sleep(1)

if __name__ == '__main__':
    thread = Thread(target=otherThread)
    thread.start()
    start_bar()
    thread.join()
    print('\nResuming all suspended apps')
    for pid in SUSPENDED:
        os.kill(int(pid), signal.SIGCONT)


