#!/usr/bin/python

from __future__ import print_function
import time
import sys
import subprocess
import os
import signal
import logging

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
  """Returns list of all process IDs for given application.
  """
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
  return app['NSApplicationName']

def suspend(prev_app):
  if name_of(prev_app) in DONT_SUSPEND_NAME:
    print(name_of(prev_app) + ' not suspended, in dont suspend list')
    return
  pids = get_pids(prev_app)
  logger.debug('Suspending %s (%s)', pids, name_of(prev_app))
  map(SUSPENDED.add, pids)
  map(lambda x: os.kill(x, signal.SIGSTOP), pids)


def resume(app):
  'Resume apps that have been suspende and arent on the do not suspend list'
  if name_of(app) in DONT_SUSPEND_NAME: 
    print(name_of(app) + ' not resumed, in dont suspend list')
    return

  pids = get_pids(app)
  for pid in pids:
    if pid not in SUSPENDED:
      break
  else:
    return
  # only resume pids that are suspended
  logger.debug('Resuming %s (%s)', pids, name_of(app))
  map(SUSPENDED.discard, pids)
  map(lambda x: os.kill(x, signal.SIGCONT), pids)
  # sometimes it won't work from the first time
  map(lambda x: os.kill(x, signal.SIGCONT), pids)

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
    time.sleep(0.5)

def suspend_my_apps(my_app_names):
  prev_app = None
  my_apps = set()
  
  while True:
    app = NSWorkspace.sharedWorkspace().activeApplication()
    if prev_app != app:
      prev_app = app
      logger.debug('Currently focused on %s', name_of(app))
      if name_of(app) in my_app_names:
        my_apps.add(app)
        resume(app)
      else:
        stop = False
        for my_app in my_apps:
          suspend(my_app)
   
def main():
  if len(sys.argv) > 1:
    my_apps = sys.argv[1:]
    print(my_apps)
    suspend_my_apps(my_apps)
  else:
    launchedApps  = NSWorkspace.sharedWorkspace().launchedApplications()
    appNames = [ app['NSApplicationName'] for app in launchedApps ]
    for appName in appNames:
        print(appName)
    suspend_bg_apps()

if __name__ == '__main__':
  try:
    main()
  except KeyboardInterrupt:
    print('\nResuming all suspended apps')
    map(lambda x: os.kill(x, signal.SIGCONT), SUSPENDED)
