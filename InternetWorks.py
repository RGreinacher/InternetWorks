#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Gui (pekingmaster@gmail.com)


import sys
from time import sleep

from PyQt4.QtGui import *
from PyQt4.QtCore import QThread, SIGNAL

import requests
import icons

import argparse
from daemonize import Daemonize


# Replace target as you want.
# We're using a static IP for Google to make sure our DNS doesn't fool us.
CHECK_TARGET = 'http://74.125.224.72/' #'http://www.google.com'


class SysTrayIcon(QSystemTrayIcon):
  def __init__(self, parent=None):
    super(SysTrayIcon, self).__init__(parent)

    self.okIcon = QIcon(':/ok.png')
    self.failIcon = QIcon(':/broken.png')

    self.initUI()

    self.checkThread = CheckThread()
    self.checkThread.start()

    self.connect(self.checkThread, SIGNAL('inet'), self.statusToggle)

  def initUI(self):
    if self.isSystemTrayAvailable():
      self.setIcon(self.okIcon)

      self.quitAction = QAction('Quit', self)

      self.trayMenu = QMenu()
      self.trayMenu.addAction(self.quitAction)
      self.connect(self.quitAction, SIGNAL('triggered()'), self.quitAll)

      self.setContextMenu(self.trayMenu)
      self.setVisible(True)

  def statusToggle(self, status):
    if status == 'OK':
      self.setIcon(self.okIcon)
    elif status == 'FAILED':
      self.setIcon(self.failIcon)

  def quitAll(self):
    self.checkThread.quit()
    self.hide()
    del self
    sys.exit(0)


class CheckThread(QThread):
  def check_connection(self):
    self.r = None
    try:
      self.r = requests.get(CHECK_TARGET, timeout=2.5)
      if self.r.status_code == 200:
        return 1
      else:
        return 0
    except:
      return 0

  def run(self):
    while 1:
      sleep(2)

      # Trigger the checking.
      ret = self.check_connection()
      if ret:
        self.emit(SIGNAL('inet'), 'OK')
      else:
        self.emit(SIGNAL('inet'), 'FAILED')

      # Clear the cache.
      if self.r:
        del self.r


# ************************************************
# non object orientated entry code goes down here:
# ************************************************
def start_internet_works():
  app = QApplication([])
  tray = SysTrayIcon(app)
  tray.show()
  sys.exit(app.exec_())

if __name__ == '__main__':
  parser = argparse.ArgumentParser(
    description = 'A system tray icon indicates \
      the Internet online & offline status'
  )
  parser.add_argument(
    '-d',
    '--daemon',
    action = 'store_true',
    dest = 'daemon',
    help = 'enables daemon mode'
  )
  args = parser.parse_args()

  if args.daemon:
    daemon = Daemonize(
      app='SleepServer Daemon',
      pid='/tmp/sleepServerDaemon.pid',
      action=start_internet_works
    )
    daemon.start()
  else:
    start_internet_works()
