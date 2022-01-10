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
from PySide.QtCore import QObject, QTimer, Signal, Slot, QUrl
from PySide import QtGui, QtNetwork

from protocol.milestone import XPMOBILE

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

class MilestoneVideoUpload(QObject):

    imageReceived = Signal(QtGui.QImage)

    def __init__(self, baseUrl, videoId, byteOrder):
        super(MilestoneVideoUpload, self).__init__()
        self.baseUrl = baseUrl
        self.videoId = videoId
        self.byteOrder = byteOrder
        self.dataBuffer = str()
        self.sendFrame()

    def getVideoId(self):
        return self.videoId

    def getImageData(self):
        return open('prova.jpg', 'rb').read()

    def sendFrame(self):

        def finished(http):
            http.deleteLater()
            self.sendFrame()

        logger.info('Send Frame')
        data = XPMOBILE.buildFrame(self.videoId, self.getImageData(), self.byteOrder)
        relativeUrl = QUrl('/XProtectMobile/Video/%s' % (self.getVideoId()))
        return MilestoneClient.request(self.baseUrl, relativeUrl, data, finished)


class MilestoneVideo(QObject):
   
    imageReceived = Signal(QtGui.QImage)
 
    def __init__(self, baseUrl, videoId, byteOrder):
        super(MilestoneVideo, self).__init__()
        self.baseUrl = baseUrl
        self.videoId = videoId
        self.byteOrder = byteOrder
        self.dataBuffer = str()
        self.videoWidget = QtGui.QLabel()
        self.requestFrame()

    def getVideoId(self):
        return self.videoId

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
        self.appendData(http.readAll())
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

    def requestFrame(self):
        relativeUrl = QUrl('/XProtectMobile/Video/%s' % (self.getVideoId()))
        return MilestoneClient.request(self.baseUrl, relativeUrl, None, self.dataReceived, self.dataReceived)

    def handleFrame(self, values):
        image = QtGui.QImage.fromData(values['FrameBytes'])
        self.imageReceived.emit(image)
        self.videoWidget.setPixmap(QtGui.QPixmap.fromImage(image))


class MilestoneClient(QObject):

    class SEQUENCE:
        USER = 1
        REFRESH = 2
        KEEPALIVE = 3
        CONNECTION = 4
        UPLOAD = 5

    @staticmethod
    def request(baseUrl, relativeUrl, body, finished, chuncked=None):
        url = baseUrl.resolved(relativeUrl)

        def chunk():
            if chuncked: chuncked(http)

        def done(errorOccurred):
            http.deleteLater()

            if errorOccurred:
                logger.error('%s errorOccurred: %r' % (url.toString(), errorOccurred))
                return

            statusCode = http.lastResponse().statusCode()
            if statusCode not in [200]:
                logger.error('%s statusCode: %r' % (url.toString(), statusCode))
                return

            finished(http)

        headers = QtNetwork.QHttpRequestHeader('POST', relativeUrl.toString())
        headers.setValue('Host', url.host())
        headers.setValue('User-Agent', 'iMilesonte')
        headers.setValue('Content-Type', 'text/xml')

        http = QtNetwork.QHttp()
        http.setHost(url.host(), port=url.port(80))
        http.done.connect(done)
        http.readyRead.connect(chunk)
        http.request(headers, body)


    connected = Signal()
    disconnected = Signal()
    videoStarted = Signal(MilestoneVideo)
    videoStopped = Signal()

    def __init__(self, baseUrl, username, password):
        super(MilestoneClient, self).__init__()
        self.baseUrl = baseUrl
        self.username = username
        self.password = password
        self.methodType = XPMOBILE.METHODTYPE.PUSH
        self.camera = dict()
        self.video = dict()
        self.connectionId = None

        def timer(intervall, slot):
            timer = QTimer()
            timer.setSingleShot(False)
            timer.setInterval(intervall * 1000)
            timer.timeout.connect(slot)
            timer.start()
    
        self.keepaliveTimer = timer(10, self.keepAlive)
        self.getviewsTimer = timer(60, self.refreshCamera)

    def getCamera(self):
        return self.camera

    def getVideoById(self, videoId):
        return self.video[videoId]

    def getVideo(self):
        return self.video

    def isConnected(self):
        return self.connectionId is not None
    
    def doConnect(self):
        self.sendCommand(XPMOBILE.connect(self.SEQUENCE.CONNECTION))

    def doDisconnect(self):
        assert self.connectionId, 'Missing connection'
        self.sendCommand(XPMOBILE.disconnect(self.SEQUENCE.CONNECTION, self.connectionId))

    def keepAlive(self):
        if self.connectionId is None: return
        self.sendCommand(XPMOBILE.liveMessage(self.SEQUENCE.KEEPALIVE, self.connectionId))

    def getViews(self):
        assert self.connectionId, 'Missing connection'
        self.sendCommand(XPMOBILE.getViews(self.SEQUENCE.CONNECTION, self.connectionId, XPMOBILE.VIEW.ALLCAMERA))

    def refreshCamera(self):
        if self.connectionId is None: return
        self.sendCommand(XPMOBILE.getViews(self.SEQUENCE.REFRESH, self.connectionId, XPMOBILE.VIEW.ALLCAMERA))

    def requestStream(self, cameraId, streamResolution, streamFPS):
        assert self.connectionId, 'Missing connection'
        assert cameraId in self.camera, 'Unknown camera: %r' % (cameraId, )
        kargs = dict(streamFPS=streamFPS, streamCompression=90)
        self.sendCommand(XPMOBILE.requestStream(self.SEQUENCE.USER, self.connectionId, self.camera[cameraId], self.methodType, streamResolution, **kargs))

    def requestStreamUpload(self):
        assert self.connectionId, 'Missing connection'
        self.sendCommand(XPMOBILE.requestStreamUpload(self.SEQUENCE.UPLOAD, self.connectionId, self.methodType))

    def closeStream(self, videoId):
        assert videoId, 'Missing video stream'
        assert self.connectionId, 'Missing connection'
        self.sendCommand(XPMOBILE.closeStream(self.SEQUENCE.USER, self.connectionId, videoId))

    def logIn(self):
        assert self.connectionId, 'Missing connection'
        self.sendCommand(XPMOBILE.logIn(self.SEQUENCE.CONNECTION, self.connectionId, self.username, self.password))

    def sendCommand(self, body):
        def finished(http):
            data = str(http.readAll())
            self.handlePacket(*XPMOBILE.parsePacket(data))

        relativeUrl = QUrl('/XProtectMobile/Communication')
        return MilestoneClient.request(self.baseUrl, relativeUrl, body, finished)

    def handlePacket(self, sequenceId, commandName, commandValues, commandLogs):
        logger.debug('Received sequenceId: %d commandName: %s' % (sequenceId, commandName))

        for commandLog in commandLogs:
            logger.warning('Received log: %s' % (commandLog, ))
            return

        if commandName == XPMOBILE.COMMAND.CONNECT:
            self.connectionId = commandValues['ConnectionId']
            self.logIn()
            return

        if commandName == XPMOBILE.COMMAND.LOGIN:
            self.getViews()
            return

        if commandName == XPMOBILE.COMMAND.GETVIEWS:
            self.camera = self.handleGetView(commandValues)
            if sequenceId == self.SEQUENCE.CONNECTION: self.connected.emit()
            return

        if commandName == XPMOBILE.COMMAND.LIVEMESSAGE:
            return

        if commandName == XPMOBILE.COMMAND.DISCONNECT:
            self.connectionId = None
            self.disconnected.emit()
            return

        if commandName == XPMOBILE.COMMAND.REQUESTSTREAM:
            print commandValues
            video = self.handleRequestStreamUpload(commandValues) if sequenceId == self.SEQUENCE.UPLOAD else self.handleRequestStream(commandValues)
            self.video[video.getVideoId()] = video
            self.videoStarted.emit(video)
            return

        if commandName == XPMOBILE.COMMAND.CLOSESTREAM:
            self.videoStopped.emit()
            return

        logger.warning('Unknown packet: %s' % (commandName, ))

    def getBaseUrl(self, values):
        assert values['Protocol'] == XPMOBILE.PROTOCOL.HTTP, 'Unknown protocol: %r' % (values['Protocol'], )
        baseUrl = QUrl()
        baseUrl.setHost(values['Address'])
        baseUrl.setPort(int(values['Port']))
        return baseUrl    

    def handleRequestStream(self, values):
        baseUrl = self.getBaseUrl(values)
        return MilestoneVideo(baseUrl, values['VideoId'], values['ByteOrder'])

    def handleRequestStreamUpload(self, values):
        baseUrl = self.getBaseUrl(values)
        return MilestoneVideoUpload(baseUrl, values['VideoId'], values['ByteOrder'])

    def handleGetView(self, values):
        camera = dict()
        for item in values['SubItems'].values():
            if item['Type'] == 'Camera':
                camera[item['Name']] = item['Id']
        return camera


class iMilestone(QtGui.QDialog):

    def __init__(self, baseUrl, username, password, cameraId, parent=None):
        QtGui.QDialog.__init__(self, parent)

        self.baseUrl = QUrl(baseUrl)
        self.username = username
        self.password = password
        self.cameraId = cameraId
        self.wantClose = False

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
        layButton.addWidget(button('Start Video', self.startVideo))
        layButton.addWidget(button('Stop Video', self.stopVideo))
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
        self.milestone.videoStarted.connect(self.onVideoStarted)
        self.milestone.videoStopped.connect(self.onVideoStopped)
        self.milestone.disconnected.connect(self.onDisconnected)
        self.connect()

    def setStatus(self, value):
        self.statusBox.setText(value)

    def connect(self):
        assert not self.milestone.isConnected(), 'Already connected'
        self.milestone.doConnect()

    def onConnected(self):
        self.setStatus('Connected')
        #if self.cameraId: self.startVideo(self.cameraId)
        self.startUpload()
        print self.milestone.getCamera()

    def disconnect(self):
        assert self.milestone.isConnected(), 'Not connected'
        self.milestone.doDisconnect()

    def onDisconnected(self):
        self.setStatus('Disconnected')
        if self.wantClose: self.close()

    def chooseCamera(self):
        cameraId, retCode = QtGui.QInputDialog.getItem(self, 'Select camera...', 'Camera Id:', self.milestone.getCamera().keys(), editable=False)
        assert retCode, 'Nothing done'
        return cameraId

    def startVideo(self, cameraId=None):
        assert self.milestone.isConnected(), 'Not connected'
        if cameraId is None: cameraId = self.chooseCamera()
        streamResolution, streamFPS = (800, 600), 5
        self.milestone.requestStream(cameraId, streamResolution, streamFPS)

    def startUpload(self):
        assert self.milestone.isConnected(), 'Not connected'
        self.milestone.requestStreamUpload()

    def onVideoStarted(self, video):
        self.setStatus('Video Started: %s' % (video.getVideoId()))

    def stopVideo(self):
        for videoId in self.milestone.getVideo():
            self.milestone.closeStream(videoId)

    def onVideoStopped(self):
        self.setStatus('Video Stopped')

    def closeEvent(self, event):
        if not self.wantClose and self.milestone.isConnected():
            self.wantClose = True
            self.disconnect()
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
