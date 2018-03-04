#!/usr/bin/python

from __future__ import print_function
import time
import sys
import subprocess
import os
import signal
import logging
#import rumps
from threading import Thread

try:
    from AppKit import NSWorkspace
except ImportError:
    print("Can't import AppKit -- maybe you're running python from brew?")
    print("Try running with Apple's /usr/bin/python instead.")
    sys.exit(1)


logger = logging.getLogger()

logger.setLevel(logging.DEBUG)
formatter = logging.Formatter(
        '%(asctime)s %(levelname)s %(name)s: %(message)s', '%b %d %H:%M:%S')
stdout = logging.StreamHandler(sys.stdout)
stdout.setFormatter(formatter)
logger.addHandler(stdout)


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

SUSPENDED = set()  #set of PIDs that has been suspended
SUSPEND_ME_NAME = set()  #set of apps user wants to suspend names
DONT_SUSPEND_NAME = ('Terminal', 'Activity Monitor') #set of apps to never suspend/resume

def name_of(app):
    if app is None:
        return None
    app_name = app['NSApplicationName']
    if sys.version_info.major < 3 and isinstance(app_name, unicode):
        # TODO handle errors instead of ignoring them
        app_name = app_name.encode("utf8", "ignore")
    return app_name

def suspend(prev_app):
    if name_of(prev_app) in DONT_SUSPEND_NAME:
        print(name_of(prev_app) + ' not suspended, in dont suspend list')
        return
    pids = get_pids(prev_app)
    logger.debug('Suspending %s (%s)', pids, name_of(prev_app))
    for pid in pids:
        SUSPENDED.add(pid)
        os.kill(int(pid), signal.SIGSTOP)


def resume(app):
    'Resume apps that have been suspended and arent on the do not suspend list'
    if name_of(app) in DONT_SUSPEND_NAME: 
        print(name_of(app) + ' not resumed, in dont suspend list')
        return

    pids = get_pids(app)
    for pid in pids:
        if pid in SUSPENDED:
            break
    else:
        return
    # only resume pids that are suspended
    logger.debug('Resuming %s (%s)', pids, name_of(app))
    for pid in pids:
        SUSPENDED.discard(pid)
        os.kill(int(pid), signal.SIGCONT)
    for pid in pids:
        os.kill(int(pid), signal.SIGCONT)

def suspend_bg_apps():
    prev_app = None

    while True:
        app = NSWorkspace.sharedWorkspace().activeApplication()
        if prev_app is None:
            prev_app = app
        if prev_app and app != prev_app:
            suspend(prev_app)
        resume(app) 
        prev_app = app
        time.sleep(0.7)

def suspend_my_apps(my_app_names):
    prev_app = None
    my_apps = set()

    print("Suspending given apps that have been launched:")
    launchedApps = NSWorkspace.sharedWorkspace().launchedApplications()
    for app in launchedApps:
        if name_of(app) in my_app_names:
            my_apps.add(app)
            suspend(app)

    print("In main loop:")
    while True:
        app = NSWorkspace.sharedWorkspace().activeApplication()
        if prev_app != app:
            logger.debug('Currently focused on %s', name_of(app))
            if name_of(app) in my_app_names:
                my_apps.add(app)  # in case app not launched initially
                resume(app)
            if name_of(prev_app) in my_app_names:
                suspend(prev_app)
            prev_app = app
        time.sleep(0.7)

def init_bar():
    launchedApps  = NSWorkspace.sharedWorkspace().launchedApplications()
    appNames = [ app['NSApplicationName'] for app in launchedApps ]
    print('Launched apps:', appNames)
    desiredApps = set()
    teststring = "hello world"
    
    rumpsClass = \
'''class AwesomeStatusBarApp(rumps.App):
'''
    menuItemString =\
'''    @rumps.clicked(%s)
    def onoff%d(self, sender):
        sender.state = not sender.state
        print(teststring)
        if sender.state:
            desiredApps.add(%s)
'''
    for i, launchedApp in enumerate(launchedApps):
        appStr = 'launchedApp[%d]' % i
        appNameStr = '\'%s\'' % launchedApp['NSApplicationName']
        rumpsClass += menuItemString % (appNameStr, i, appStr)
    #print(rumpsClass)
    return rumpsClass


def main():
    if len(sys.argv) > 1:
        my_app_names = sys.argv[1:]
        print(my_app_names)
        #thread = Thread(target=suspend_my_apps, args=my_app_names)
        #thread.start()
        #init_bar()
        #AwesomeStatusBarApp("NapMyApp").run()
        #thread.join()
        suspend_my_apps(my_app_names)
    else:
        launchedApps  = NSWorkspace.sharedWorkspace().launchedApplications()
        appNames = [ app['NSApplicationName'] for app in launchedApps ]
        for appName in appNames:
            print(appName)
        suspend_bg_apps()

if __name__ == '__main__':
    try:
        #exec(init_bar())
        main()
    except KeyboardInterrupt:
        print('\nResuming all suspended apps')
        for pid in SUSPENDED:
            os.kill(int(pid), signal.SIGCONT)

