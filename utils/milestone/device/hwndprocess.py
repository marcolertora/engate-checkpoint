#!/usr/bin/env python
# -*- Mode: Python; tab-width: 4 -*-
#
# HwndProcess
#
# Copyright (c) 2014 Infoporto La Spezia S.r.l.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTIBILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# for more details.
#

import ctypes
import win32gui
import win32process
from PySide.QtCore import QTimer, Signal, Slot, QProcess
from PySide.QtGui import QPixmap, QApplication

class HwndProcess(QProcess):

    @staticmethod
    def getHwndListByPid(wantedPid):
        def callback(hwnd, hwndList):
            if not win32gui.IsWindowVisible(hwnd) or not win32gui.IsWindowEnabled(hwnd): return True
            dummy, pid = win32process.GetWindowThreadProcessId(hwnd)
            if not pid == wantedPid: return True
            hwndList.append(HwndProcess.createHwnd(hwnd))
            return True
        hwndList = list()
        win32gui.EnumWindows(callback, hwndList)
        return hwndList

    @staticmethod
    def createHwnd(value):
        ctypes.pythonapi.PyCObject_FromVoidPtr.restype = ctypes.py_object
        ctypes.pythonapi.PyCObject_FromVoidPtr.argtypes = [ctypes.c_void_p]
        hwnd = ctypes.pythonapi.PyCObject_FromVoidPtr(value)
        ctypes.pythonapi.Py_IncRef.argtypes = [ctypes.py_object]
        ctypes.pythonapi.Py_IncRef(hwnd)
        return hwnd

    displayed = Signal()

    def __init__(self, cmdFile, cmdArgs=None, parent=None):
        super(HwndProcess, self).__init__(parent)
        self.cmdFile = cmdFile
        self.cmdArgs = cmdArgs if cmdArgs is not None else list()
        self.timerHwndInterval = 1000
        self.hwndList = list()
        self.hwndMain = None
        self.timerHwnd = QTimer()
        self.timerHwnd.setInterval(self.timerHwndInterval)
        self.timerHwnd.timeout.connect(self.refreshHwndList)
        self.started.connect(self.onStarted)
        self.finished.connect(self.onFinished)
        self.start(self.cmdFile, self.cmdArgs)

    def onStarted(self):
        self.timerHwnd.start()

    def onFinished(self):
        self.timerHwnd.stop()

    def refreshHwndList(self):
        hwndList = self.getHwndList()
        if not len(self.hwndList) and len(hwndList):
            self.hwndMain = hwndList[0]
            self.displayed.emit()
        self.hwndList = hwndList

    def getDummyImage(self):
        return QPixmap(1, 1)

    def getScreenshot(self):
        hwnd = self.getMainHwnd()
        return  QPixmap.grabWindow(hwnd) if hwnd else self.getDummyImage()

    def getHwndList(self):
        return HwndProcess.getHwndListByPid(self.pid())

    def getMainHwnd(self):
        return self.hwndMain
        if len(self.hwndList): return self.hwndList[0]


def showCamera(baseUrl, username, password, cameraId):
    app = QApplication(sys.argv)
    win = iMilestone(baseUrl, username, password, cameraId)
    win.show()
    app.exec_()
    return win.result()

if __name__ == '__main__':
    baseUrl = 'http://172.16.2.11:8081/'
    username, password = 'marco.lertora', 'infoporto'
    cameraId = None
    if len(sys.argv) > 1:  cameraId = sys.argv[1]
    showCamera(baseUrl, username, password, cameraId)
