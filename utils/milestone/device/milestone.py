#!/usr/bin/env python
# -*- Mode: Python; tab-width: 4 -*-
#
# Milestone
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

import sys
import logging
from time import time
from PySide.QtCore import QObject, QTimer, Signal, Slot, QUrl
from PySide.QtCore import QBuffer, QIODevice
from PySide import QtGui, QtNetwork

from hwndprocess import HwndProcess
from protocol.milestone import XPMOBILE

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

class MilestoneVideoUpload(QObject):

    def __init__(self, client, baseUrl, videoId, byteOrder):
        super(MilestoneVideoUpload, self).__init__()
        self.client = client
        self.baseUrl = baseUrl
        self.videoId = videoId
        self.byteOrder = byteOrder
        self.imgFormat = 'JPEG'
        self.dataBuffer = str()
		self.timer = QTimer()
        
    def getVideoId(self):
        return self.videoId

	def doUploadStart(self, retrieveFunc, intervall=100):
		def pushFrame():
			if not self.timer.isActive(): return
			self.sendFrame(retrieveFunc())
			
		self.timer.start()
		self.timer.setInterval(intervall)
		self.timer.timeout.connect(pushFrame)
		
	def doUploadStop(self):
		self.timer.stop()
	
	def doVideoStop(self, callback=None):
        self.client.doVideoStop(self.getVideoId(), callback=callback)
		
    def sendFrame(self, pixmap, callback=None, errback=None):

        def finished(http):
            if callback: callback()

        def failure(message):
            logger.warning(message)
            self.client.failure.emit(message)
            if errback: errback(message)

        data = XPMOBILE.buildFrame(self.videoId, MilestoneClient.pixmapToData(pixmap, self.imgFormat), self.byteOrder)
        relativeUrl = QUrl('/XProtectMobile/Video/%s' % (self.getVideoId()))
        return MilestoneClient.requestUrl(self.baseUrl, relativeUrl, data, callback=finished, errback=failure)


class MilestoneVideoDownload(QObject):
   
    imageReceived = Signal(QtGui.QPixmap)
 
    def __init__(self, client, baseUrl, videoId, byteOrder):
        super(MilestoneVideoDownload, self).__init__()
        self.client = client
        self.baseUrl = baseUrl
        self.videoId = videoId
        self.byteOrder = byteOrder
        self.dataBuffer = str()
        self.videoWidget = QtGui.QLabel()
        self.requestFrame()

    def getVideoId(self):
        return self.videoId

    def doVideoStop(self, callback=None):
        self.client.doVideoStop(self.getVideoId(), callback=callback)

    def getWidget(self):
        return self.videoWidget

    def appendData(self, data):
        self.dataBuffer = self.dataBuffer + data

    def hasData(self):
        return len(self.dataBuffer) > 0

    def getData(self):
        return self.dataBuffer

    def setData(self, data):
        self.dataBuffer = data

    def dataReceived(self, http):
        self.appendData(str(http.readAll()))
        while self.hasData():
            try:
                values, trail = XPMOBILE.parseFrame(self.getVideoId(), self.getData(), self.byteOrder)
            except XPMOBILE.IncompletePacket: 
                return
            except:
                http.abort()
                raise

            self.handleFrame(values)
            self.setData(trail)

    def requestFrame(self, errback=None):
        relativeUrl = QUrl('/XProtectMobile/Video/%s' % (self.getVideoId()))
        return MilestoneClient.requestUrl(self.baseUrl, relativeUrl, None, callback=self.dataReceived, errback=errback, chuncking=self.dataReceived)

    def handleFrame(self, values):
        pixmap = QtGui.QPixmap.fromData(values['FrameBytes'])
        self.imageReceived.emit(pixmap)
        self.videoWidget.setPixmap(pixmap)


class MilestoneClient(QObject):

    @staticmethod
    def pixmapToData(pixmap, imgFormat):
        imgBuffer = QBuffer()
        imgBuffer.open(QIODevice.ReadWrite)
        pixmap.save(imgBuffer, imgFormat)
        return imgBuffer.data()

    @staticmethod
    def formatLog(logs):
        separator = ', '
        return separator.join(logs)

    @staticmethod
    def requestUrl(baseUrl, relativeUrl, body, callback=None, errback=None, chuncking=None):
        url = baseUrl.resolved(relativeUrl)

        def chunck():
            if chuncking: chuncking(http)

        def done(errorOccurred):
            http.deleteLater()

            if errorOccurred:
                message = 'Error: [%s] %r' % (url.toString(), errorOccurred)
                if errback: errback(message)
                return

            statusCode = http.lastResponse().statusCode()
            if statusCode not in [200]:
                message = 'Error: [%s] %r' % (url.toString(), statusCode)
                if errback: errback(message)
                return
    
            if callback: callback(http)

        headers = QtNetwork.QHttpRequestHeader('POST', relativeUrl.toString())
        headers.setValue('Host', url.host())
        headers.setValue('User-Agent', 'iMilesonte')
        headers.setValue('Content-Type', 'text/xml')

        http = QtNetwork.QHttp()
        http.setHost(url.host(), port=url.port(80))
        http.done.connect(done)
        http.readyRead.connect(chunck)
        http.request(headers, body)


    connected = Signal()
    disconnected = Signal()
    failure = Signal(str)

    def __init__(self, baseUrl, username, password, parent=None):
        super(MilestoneClient, self).__init__(parent)
        self.baseUrl = baseUrl
        self.username = username
        self.password = password
        self.methodType = XPMOBILE.METHODTYPE.PUSH
        self.camera = dict()
        self.video = dict()
        self.sequenceId = 1
        self.connectionId = None
        self.reconnect = False
        self.reconnectIntervall = 3

        def timer(intervall, slot):
            timer = QTimer()
            timer.setSingleShot(False)
            timer.setInterval(intervall * 1000)
            timer.timeout.connect(slot)
            return timer
    
        self.keepaliveLast = None
        self.keepaliveIntervall = 10
        self.watchdogIntervall = 20
        self.getviewsIntervall = 60
        self.watchdogTimer = timer(self.watchdogIntervall, self.doWatchDog)
        self.keepaliveTimer = timer(self.keepaliveIntervall, self.doKeepAlive)
        self.getviewsTimer = timer(self.getviewsIntervall, self.doRefreshCamera)

    def getSequenceId(self):
        return self.sequenceId

    def getConnectionId(self):
        assert self.isConnected(), 'No connection'
        return self.connectionId

    def setConnectionId(self, connectionId=None):
        self.connectionId = connectionId

    def getCamera(self):
        return self.camera

    def getVideoById(self, videoId):
        return self.video[videoId]

    def getVideo(self):
        return self.video

    def isConnected(self):
        return self.connectionId is not None
    
    def doConnect(self, reconnect=False, callback=None, errback=None):
        self.reconnect = reconnect
        self._doConnect(callback=callback, errback=errback)

    def _doConnect(self, callback=None, errback=None):
        def failure1(message):
            self._doDisconnect(callback=lambda: failure2(message))
        def failure2(message):
            if errback: errback(message)
        def step1():
            self.sendCommand(XPMOBILE.connect(self.getSequenceId()), callback=step2, errback=failure1)
        def step2(values):
            self.setConnectionId(values['ConnectionId'])
            self.sendCommand(XPMOBILE.logIn(self.getSequenceId(), self.getConnectionId(), self.username, self.password), callback=step3, errback=failure1)
        def step3(values):
            self.sendCommand(XPMOBILE.getViews(self.getSequenceId(), self.getConnectionId(), XPMOBILE.VIEW.ALLCAMERA), callback=step4, errback=failure1)
        def step4(values):
            self.camera = self.getCameraFromResponse(values)
            self.keepaliveLast = time()
            self.watchdogTimer.start()
            self.keepaliveTimer.start()
            self.getviewsTimer.start()
            self.connected.emit()
            if callback: callback()
        step1()

    def doDisconnect(self, callback=None):
        self.reconnect = False
        self._doDisconnect(callback=callback)

    def _doDisconnect(self, callback=None):
        def step1():
            self.doVideoStopAll(callback=step2)
        def step2():
            if not self.isConnected(): step3()
            else: self.sendCommand(XPMOBILE.disconnect(self.getSequenceId(), self.getConnectionId()), callback=lambda x: step3(), errback=lambda x: step3())
        def step3():
            self.setConnectionId()
            self.watchdogTimer.stop()
            self.keepaliveTimer.stop()
            self.getviewsTimer.stop()
            self.disconnected.emit()
            if callback: callback()
            if self.reconnect: QTimer.singleShot(self.reconnectIntervall * 1000, step4)
        def step4():
            if self.reconnect: self._doConnect()
        step1()

    def doWatchDog(self):
        if (time() - self.keepaliveLast) > (self.keepaliveIntervall * 2):
            self._doDisconnect()

    def doKeepAlive(self):
        def step1():
            self.sendCommand(XPMOBILE.liveMessage(self.getSequenceId(), self.getConnectionId()), callback=step2)
        def step2(values):
            self.keepaliveLast = time()
        step1()

    def doRefreshCamera(self):
        def step1():
            self.sendCommand(XPMOBILE.getViews(self.getSequenceId(), self.getConnectionId(), XPMOBILE.VIEW.ALLCAMERA), callback=step2)
        def step2(values):
            self.camera = self.getCameraFromResponse(values)
        step1()

    def doVideoStart(self, cameraId, streamResolution, streamFPS, callback=None, errback=None):
        def step1():
            commandKargs = dict(streamFPS=streamFPS, streamCompression=90)
            command = XPMOBILE.requestStream(self.getSequenceId(), self.getConnectionId(), self.camera[cameraId], self.methodType, streamResolution, **commandKargs)
            self.sendCommand(command, callback=step2, errback=errback)
        def step2(values):
            video = MilestoneVideoDownload(self, self.getBaseUrlFromResponse(values), values['VideoId'], values['ByteOrder'])
            self.video[video.getVideoId()] = video
            if callback: callback(video)
        step1()

    def doVideoUpload(self, callback=None, errback=None):
        def step1():
            self.sendCommand(XPMOBILE.requestStreamUpload(self.getSequenceId(), self.getConnectionId(), self.methodType), callback=step2, errback=errback)
        def step2(values):
            video = MilestoneVideoUpload(self, self.getBaseUrlFromResponse(values), values['VideoId'], values['ByteOrder'])
            self.video[video.getVideoId()] = video
            if callback: callback(video)
        step1()

    def doVideoStop(self, videoId, callback=None):
        def step1():
            self.sendCommand(XPMOBILE.closeStream(self.getSequenceId(), self.getConnectionId(), videoId), callback=lambda x: step2(), errback=lambda x: step2())
        def step2():
            video = self.video.pop(videoId)
            if callback: callback(video)
        step1()

    def doVideoStopAll(self, callback=None):
        def step1():
            if not len(self.video) and callback: callback()
        for videoId in self.video.keys():
            self.doVideoStop(videoId, callback=lambda x: step1())
        step1()

    def sendCommand(self, body, callback=None, errback=None):
        def failure(message):
            message = 'Error sending command'
            logger.warning(message)
            if errback: errback(message)
            self.failure.emit(message)
        def finished(http):
            sequenceId, command, values, logs = XPMOBILE.parse_packet(str(http.readAll()))
            logger.debug('Received sequenceId: %d command: %s' % (sequenceId, command))
            if len(logs): failure(MilestoneClient.formatLog(logs))
            elif callback: callback(values)

        relativeUrl = QUrl('/XProtectMobile/Communication')
        return MilestoneClient.requestUrl(self.baseUrl, relativeUrl, body, callback=finished, errback=failure)

    def getBaseUrlFromResponse(self, values):
        assert values['Protocol'] == XPMOBILE.PROTOCOL.HTTP, 'Unknown protocol: %r' % (values['Protocol'], )
        baseUrl = QUrl()
        baseUrl.setHost(values['Address'])
        baseUrl.setPort(int(values['Port']))
        return baseUrl    

    def getCameraFromResponse(self, values):
        camera = dict()
        for item in values['SubItems'].values():
            if not item['Type'] == 'Camera': continue
            camera[item['Name']] = item['Id']
        return camera


class iMilestone(QtGui.QDialog):

    def __init__(self, baseUrl, username, password, cameraId, parent=None):
        QtGui.QDialog.__init__(self, parent)

        self.baseUrl = QUrl(baseUrl)
        self.username = username
        self.password = password
        self.cameraId = cameraId

        # display windows
        self.setWindowTitle('Milestone Client: %s@%s' % (self.username, self.password))

        # create label for webcam and status
        self.statusBox = QtGui.QLabel()
        self.layCamera = QtGui.QVBoxLayout()

        def button(label, slot):
            button = QtGui.QPushButton(label)
            button.setFixedHeight(30)
            button.clicked.connect(slot)
            return button

        layButton = QtGui.QHBoxLayout()
        layButton.addWidget(button('Connect', self.connect))
        layButton.addWidget(button('Start Video', self.videoStart))
        layButton.addWidget(button('Stop Video', self.videoStop))
		layButton.addWidget(button('Start Push', self.videoUpload))
        layButton.addWidget(button('Disconnect', self.disconnect))

        # append to windows
        layMain = QtGui.QVBoxLayout(self)
        layMain.addWidget(self.statusBox)
        layMain.addLayout(self.layCamera)
        layMain.addLayout(layButton)

        self.resize(200,300)
        self.showNormal()

        # connect milestone
        self.milestone = MilestoneClient(self.baseUrl, self.username, self.password)
        self.milestone.connected.connect(self.onConnected)
        self.milestone.failure.connect(self.onFailure)
        self.milestone.disconnected.connect(self.onDisconnected)
        self.connect()

    def setStatus(self, value):
        self.statusBox.setText(value)

    def onFailure(self, message):
        self.setStatus(message)

    def connect(self):
        def done():
            if not self.cameraId: return
            if self.cameraId == 'PUSH': self.videoUpload()
			else: self.videoStart(self.cameraId)
        if self.milestone.isConnected(): return
        self.milestone.doConnect(reconnect=True, callback=done)

    def onConnected(self):
        self.setStatus('Connected')

    def disconnect(self):
        if not self.milestone.isConnected(): return
        self.milestone.doDisconnect()

    def onDisconnected(self):
        self.setStatus('Disconnected')

    def chooseCamera(self):
        assert self.milestone.isConnected(), 'Need to be connected'
        cameraId, retCode = QtGui.QInputDialog.getItem(self, 'Select camera...', 'Camera Id:', self.milestone.getCamera().keys(), editable=False)
        return cameraId if retCode else None

    def videoStart(self, cameraId=None):
        def done(video):
            self.setStatus('Video Started: %s' % (video.getVideoId()))
            self.layCamera.addWidget(video.getWidget())
        if not self.milestone.isConnected(): return
        if cameraId is None: cameraId = self.chooseCamera()
        if cameraId is None: return
        streamResolution, streamFPS = (800, 600), 5
        self.milestone.doVideoStart(cameraId, streamResolution, streamFPS, callback=done)
			
    def videoUpload(self, filename='calc.exe'):
	
		def startUpload(video, process):
			video.doUploadStart(process.getScreenshot)
	
		def stopUpload(video):
			video.doUploadStop()
			video.doVideoStop()
	
        def videoUpload(video):
			process = HwndProcess(filename)
			process.displayed.connect(lambda: startUpload(video, process))
			process.finished.connect(lambda: stopUpload(video))
		if not self.milestone.isConnected(): return
        self.milestone.doVideoUpload(callback=videoUpload)		

    def videoStop(self):
        def done():
            self.setStatus('All video Stopped')
        if not self.milestone.isConnected(): return
        self.milestone.doVideoStopAll(callback=done)

    def closeEvent(self, event):
        if not self.milestone.isConnected(): return
        self.milestone.doDisconnect(callback=self.close)
        event.ignore()

def showCamera(baseUrl, username, password, cameraId):
    app = QtGui.QApplication(sys.argv)
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
