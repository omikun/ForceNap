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


SUSPENDED = set()


def main():
  prev_app = None

  while True:
    app = NSWorkspace.sharedWorkspace().activeApplication()
    if prev_app is None:
      prev_app = app
    if app != prev_app:
      pids = get_pids(prev_app)
      logger.debug('Suspending %s (%s)', pids, prev_app['NSApplicationName'])
      map(SUSPENDED.add, pids)
      map(lambda x: os.kill(x, signal.SIGSTOP), pids)

      pids = get_pids(app)
      logger.debug('Resuming %s (%s)', pids, app['NSApplicationName'])
      map(SUSPENDED.discard, pids)
      map(lambda x: os.kill(x, signal.SIGCONT), pids)
      # sometimes it won't work from the first time
      map(lambda x: os.kill(x, signal.SIGCONT), pids)
      prev_app = app
    time.sleep(0.5)


if __name__ == '__main__':
  try:
    main()
  except KeyboardInterrupt:
    map(lambda x: os.kill(x, signal.SIGCONT), SUSPENDED)
