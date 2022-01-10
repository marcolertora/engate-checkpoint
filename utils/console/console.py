#! /usr/bin/env python
# -*- Mode: fPython; tab-width: 4 -*-
#
# Software Controllo Accessi
#
# Copyright (c) 2010-2011 Netfarm S.r.l.
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

import os, sys

from ConfigParser import ConfigParser
from PySide import QtCore, QtGui, QtNetwork
from types import StringType, DictType, ListType

import cPickle as pickle
from ui.console import Ui_Lane

#from milestone import MilestoneClient

class SplashDialog(QtGui.QDialog):

    closeIntervall = 5

    def __init__(self, parent=None):
        super(SplashDialog, self).__init__(parent)
        self.setWindowFlags(QtCore.Qt.SplashScreen | QtCore.Qt.WindowStaysOnTopHint)
        if self.closeIntervall: QtCore.QTimer(self).singleShot(self.closeIntervall * 1000, self.doClose)
        self.resize(600, 200)

    def doClose(self):
        self.close()


class DialogCamera(SplashDialog):

    closeInterval = None

    def __init__(self, milestoneVideo, closeIntervall, parent=None):
        self.milestoneVideo = milestoneVideo
        self.closeIntervall = closeIntervall
        super(DialogCamera, self).__init__(parent)
        closeButton = QtGui.QPushButton(self.tr('Close'))
        closeButton.clicked.connect(self.doClose)
        self.mainLayout = QtGui.QVBoxLayout()
        self.mainLayout.addWidget(milestoneVideo.getWidget())
        self.mainLayout.addWidget(closeButton)
        self.setLayout(self.mainLayout)
        self.show()

    def doClose(self, callback=None):
        def close(video): 
            self.close()
            if callback: callback()
        self.milestoneVideo.doVideoStop(callback=close)


class Lane(QtGui.QGroupBox, Ui_Lane):

    DISCONNECTED, READY, NOT_READY = range(3)

    def __init__(self, parent, lane_id, priority, flags):
        QtGui.QGroupBox.__init__(self, parent)

        self.console = parent
        self.lane_id = lane_id
        self.priority = priority
        self.compact = 'COMPACT' in flags
        self.imageurl = None
        self.status = None
        self.gatelink = True
        self.laneready = False
        self.laneinfo = dict()
        self.transitinfo = dict()
        self.setupUi(self)

        def cleanup():
            self.cleanupTimer.stop()
            self.setReady()

        self.cleanupTimer = QtCore.QTimer()
        self.cleanupTimer.setSingleShot(False)
        self.cleanupTimer.timeout.connect(cleanup)

        def timeout():
            self.setDisconnected()
            self.watchdogCount += 1
            if self.watchdogCount > 10: self.detach()

        self.watchdogCount = 0
        self.watchdogTimer = QtCore.QTimer()
        self.watchdogTimer.setSingleShot(False)
        self.watchdogTimer.setInterval(Configs.watchdog * 1000)
        self.watchdogTimer.timeout.connect(timeout)
        self.resetWatchDog()
        self.setDisconnected()
        if False: self.addToolbar()

    def addToolbar(self):
        self.addButton(self.onCamera, pixmap=Resources.car)
        self.addButton(self.onOpen, pixmap=Resources.padlock)

    def onOpen(self):
        pass

    def onCamera(self):
        cameraId = 'CAM001'
        self.console.startVideo(cameraId)

    def addButton(self, slot, label=None, pixmap=None):
        button = QtGui.QPushButton()
        if label:
            button.setLabel(label)
        if pixmap:
            button.setIcon(QtGui.QIcon(pixmap))
            button.setIconSize(QtCore.QSize(30,30))
        button.setFixedSize(QtCore.QSize(40,40))
        button.clicked.connect(slot)
        self.buttonLayout.addWidget(button, alignment=QtCore.Qt.AlignLeft)

    def clear(self):
        self.clearPermission()
        self.qlPlate.clear()
        self.qlStatus.clear()

    def clearPermission(self):
        self.clearPermissionList()

    def detach(self):
        self.watchdogTimer.stop()
        self.console.removeLane(self)
        self.deleteLater()

    def isCompact(self):
        return self.compact

    def log(self, message):
        entry = u'%s %s' % (QtCore.QDateTime.currentDateTime().toString(u'hh:mm:ss'), message)
        lines = self.qteLog.toPlainText().split(Configs.CR)
        lines.append(entry)
        lines = lines[-Configs.loglines:]
        self.qteLog.setPlainText(Configs.CR.join(lines))
        scroll = self.qteLog.verticalScrollBar()
        scroll.setSliderPosition(scroll.maximum())

    def updateStatus(self, text, pixmap, log=True):
        if log: self.log(text)
        self.qlStatus.setText(text)
        self.qlStatusImage.setPixmap(pixmap)

    def resetWatchDog(self):
        self.watchdogCount = 0
        self.watchdogTimer.start()

    def setReady(self):
        self.status = Lane.READY
        self.resetWatchDog()
        self.clear()
        self.updateStatus(self.tr('Ready'), Resources.red, log=False)

    def setNotReady(self):
        self.status = Lane.NOT_READY
        self.resetWatchDog()
        self.clear()
        self.updateStatus(self.tr('Waiting for devices'), Resources.yellow, log=False)

    def setDisconnected(self):
        self.status = Lane.DISCONNECTED
        self.clear()
        self.updateGateLink(True)
        self.updateStatus(self.tr('Disconnected'), Resources.off, log=False)

    def getImage(self, relativeUrl, callback):

        url = self.imageurl.resolved(relativeUrl)

        def finished(errorOccurred):
            http.deleteLater()

            if errorOccurred:
                print '%s errorOccurred: %r' % (url.toString(), errorOccurred)
                callback(Resources.nopicture)
                return

            statusCode = http.lastResponse().statusCode()
            if statusCode not in [200]:
                print '%s statusCode: %r' % (url.toString(), statusCode)
                callback(Resources.nopicture)
                return

            picture = QtGui.QPixmap()
            picture.loadFromData(http.readAll())
            callback(picture)

        headers = QtNetwork.QHttpRequestHeader('GET', relativeUrl.toString())
        headers.setValue('Host', url.host())
        headers.setValue('User-Agent', str(Configs.APPNAME))

        http = QtNetwork.QHttp()
        http.setHost(url.host(), port=url.port(80))
        http.done.connect(finished)
        http.request(headers)

    def addPermission(self, permission, permission_key):
        def _addPermission(image):
            self.addPermissionWidget(permission_key, permission, image, self.transitinfo)
            self.log(permission['people_fullname'])

        people_id = permission.get('people_id')

        if permission['ownertype_id'] == 'VEHICLE':
            _addPermission(Resources.car)
            return

        if self.imageurl is None or people_id is None:
            _addPermission(Resources.nopicture)
            return

        relativeUrl = QtCore.QUrl('/getUserImage?people_id=%d' % (people_id))
        self.getImage(relativeUrl, _addPermission)

    def addImagePermission(self, attachment_id, permission_key):

        def _addImagePermission(picture):
            self.addImagePermissionWidget(permission_key, picture)

        if self.imageurl is None or attachment_id is None:
            _addImagePermission(Resources.nopicture)
            return

        relativeUrl = QtCore.QUrl('/getAttachment?attachment_id=%s' % (attachment_id))
        self.getImage(relativeUrl, _addImagePermission)

    def addPlate(self, plate_code):
        if not plate_code: return
        plates = self.qlPlate.text().split(Configs.CR)
        plates.append(plate_code)
        plates = plates[-5:]
        self.qlPlate.setText(Configs.CR.join(plates))

    def updateLaneReady(self, laneready):
        if self.laneready == laneready: return
        self.laneready = laneready

        if laneready: self.setReady()
        else: self.setNotReady()

    def updateTitle(self):
        title = u'%(gate_name)s %(lane_name)s - %(lanetype_name)s %(direction_name)s' % self.laneinfo
        if not self.gatelink: title = u'[%s] %s' % (self.tr('ISOLATED'), title)
        self.setTitle(title)

    def updateLaneInfo(self, info):
        laneinfo = {
            'lane_name'         : info['lane_name'],
            'gate_name'         : info['gate_name'],
            'lanetype_name'     : info['lanetype_name'],
            'direction_name'    : info['direction_name'],
            'securitylevel_name': info['securitylevel_name'],
            'lanestatus_name'   : info['lanestatus_name'],
            'antipassback'      : info['antipassback'],
            'automa_id'         : info['automa_id'],
        }

        if laneinfo == self.laneinfo: return
        self.laneinfo = laneinfo

        self.updateTitle()

        items = [
            (self.tr('Security'), laneinfo['securitylevel_name']),
            (self.tr('Status'), laneinfo['lanestatus_name']),
            (self.tr('Antipassback'), self.tr('Enabled') if laneinfo['antipassback'] else self.tr('Disabled')),
            (self.tr('Automaton'), laneinfo['automa_id']),
        ]
        self.qlLaneInfo.setText(Configs.CR.join([u'%s: %s' % x for x in items]))

    def updateGateLink(self, gatelink):
        if self.gatelink == gatelink: return
        self.gatelink = gatelink

        self.updateTitle()

    def onMsgKeepAlive(self, *args, **kw):
        self.resetWatchDog()
        self.imageurl = QtCore.QUrl(kw['imageurl'])
        self.updateLaneReady(kw['ready'])
        self.updateLaneInfo(kw)
        self.updateGateLink(kw['gatelink'])

    def onMsgSetTransitDirection(self, *args, **kw):
        self.transitinfo['transitdirection_name'] = kw['transitdirection_name']
        self.updateDirectionPermissionWidget(self.transitinfo)
        
    def onMsgSetTransitStatus(self, *args, **kw):
        self.cleanupTimer.stop()
        timeout = kw['timeout']
        status = kw['status']
        pixmap = getattr(Resources, kw['color']) if hasattr(Resources, kw['color']) else Resources.off
        self.updateStatus(status, pixmap)
        if timeout != 0:
            self.cleanupTimer.setInterval((timeout or Configs.cleanup) * 1000)
            self.cleanupTimer.start()

    def onMsgAddPermission(self, *args, **kw):
        self.addPermission(kw['permission'], kw['permission_key'])

    def onMsgCleanPermissions(self, *args, **kw):
        self.clearPermission()

    def onMsgAddAttachment(self, *args, **kw):
        pass

    def onMsgAddPermissionAttachment(self, *args, **kw):
        self.addImagePermission(kw['attachment_id'], kw['permission_key'])

    def onMsgUpdateTransitItem(self, *args, **kw):
        pass
        
    def onMsgAddTransitItem(self, *args, **kw):
        titem = kw['titem']
        titem_code = kw['titem_code']
        titemclass_id = kw['titemclass_id']

        if titemclass_id == 'Plate': 
            self.addPlate(titem_code)
            return

        assert False, 'unknown titemclass_id :%s' % titemclass_id            

    def onMsgStartTransit(self, *args, **kw):
        self.log(self.tr('New Transit'))
        self.transitinfo = dict()
        self.setReady()

    def onMsgEndTransit(self, *args, **kw):
        pass

    def onMsgText(self, *args, **kw):
        self.log(kw['text'])

    def onMsgReset(self, *args, **kw):
        self.setReady()

    def onMsgAttachLane(self, *args, **kw):
        pass

    def onMsgDetachLane(self, *args, **kw):
        self.detach()

    def onMsgRefreshLane(self, *args, **kw):
        pass


class Console(QtGui.QMainWindow):

    @staticmethod
    def fixUnicode(value):
        if type(value) == DictType:
            for k, v in value.items():
                value[k] = Console.fixUnicode(v)

        if type(value) == ListType:
            value = [Console.fixUnicode(x) for x in value]

        if type(value) == StringType:
            value = value.decode('utf-8', 'ignore')

        return value

    def __init__(self, parent=None):
        super(Console, self).__init__(parent)
        QtGui.QApplication.setStyle(QtGui.QStyleFactory.create(Configs.style))

        self.resize(300, 10)
        self.setWindowTitle(self.tr('Console'))
        self.setWindowIcon(Resources.icon)
        if Configs.fullscreen: self.showFullScreen()

        self.laneList = dict()
        self.layout = QtGui.QGridLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.centralwidget = QtGui.QWidget(self)
        self.centralwidget.setLayout(self.layout)
        self.setCentralWidget(self.centralwidget)
        self.sock = QtNetwork.QUdpSocket()
        self.sock.bind(Configs.listenport)
        self.connect(self.sock, QtCore.SIGNAL('readyRead()'), self.receiveMsg)

    #    self.dialogCamera = None
    #    self.dialogCameraCloseIntervall = 10
    #    self.milestoneBaseUrl = QtCore.QUrl('http://172.16.2.11:8081')
    #    self.milestoneUser = 'marco.lertora'
    #    self.milestonePassword = 'infoporto'
    #    self.streamResolution = (800,600)
    #    self.streamFPS = 5

    #    self.milestone = MilestoneClient(self.milestoneBaseUrl, self.milestoneUser, self.milestonePassword)
    #    self.milestone.doConnect(reconnect=True)
    #    self.milestone.connected.connect(self.startUpload)

    #def startUpload(self):
    #    def videoUpload(video):
    #        #pixmap = QtGui.QPixmap.grabWindow(self.winId())
    #        pixmap = Resources.car
    #        if len(self.laneList): 
    #            widget = self.laneList.values()[0]
    #            pixmap = QtGui.QPixmap.grabWidget(widget)
    #        print pixmap.size(), pixmap
    #        video.sendFrame(pixmap, callback=lambda: videoUpload(video))
    #    self.milestone.doVideoUpload(callback=videoUpload)
			
    #def startVideo(self, cameraId):
    #    def videoStarted(video):
    #        self.dialogCamera = DialogCamera(video, closeIntervall=self.dialogCameraCloseIntervall)
    #        self.dialogCamera.exec_()
    #        self.dialogCamera = None
    #    def videoStart():
    #        if not self.milestone.isConnected(): return
    #        self.milestone.doVideoStart(cameraId, self.streamResolution, self.streamFPS, callback=videoStarted)
    #    if self.dialogCamera: self.dialogCamera.doClose(callback=videoStart)
    #    else: videoStart()

    #def closeEvent(self, event):
    #    if self.milestone.isConnected():
    #        event.ignore()
    #        self.milestone.doDisconnect(callback=self.close)

    def paintEvent(self, pe):
        painter = QtGui.QPainter(self)
        painter.drawTiledPixmap(self.rect(), Resources.tile)
        super(Console, self).paintEvent(pe)

    def centerWindow(self):
        if self.isFullScreen(): return
        desktop = QtGui.QApplication.desktop().availableGeometry()
        size = self.frameGeometry().size()
        rect = QtGui.QStyle.alignedRect(QtCore.Qt.LeftToRight, QtCore.Qt.AlignCenter, size, desktop)
        self.move(rect.topLeft())

    def addLane(self, lane_id, priority, flags):
        lane = Lane(self, lane_id, priority, flags)
        self.laneList[lane_id] = lane
        self.redrawLanes()
        return lane

    def getLane(self, lane_id):
        return self.laneList.get(lane_id)

    def redrawLanes(self):
        lanes = sorted(self.laneList.values(), key=lambda k: k.priority)
        for lane in lanes: self.layout.removeWidget(lane)

        position = 0
        for lane in lanes:
            if not lane.isCompact() and (position % 2 != 0):
                position += 1

            col, row = divmod(position, 2)
            if lane.isCompact():
                self.layout.addWidget(lane, row, col, alignment=QtCore.Qt.AlignTop)
                position += 1
            else:
                self.layout.addWidget(lane, row, col, 2, 1)
                position += 2

    def removeLane(self, lane):
        self.laneList.pop(lane.lane_id)
        self.redrawLanes()

    def receiveMsg(self):
        data, peer, port = self.sock.readDatagram(1456)
        msg = Console.fixUnicode(pickle.loads(data.data()))

        lane = self.getLane(msg['lane_id'])

        if not lane:
            lane = self.addLane(msg['lane_id'], msg['priority'], msg['lane_flags'])

        if lane.priority != msg['priority']:
            self.laneList[msg['lane_id']].priority = msg['priority']
            self.redrawLanes()

        if not hasattr(lane, 'onMsg' + msg['type']):
            raise Exception('Missing handler for message: %s' % msg['type'])

        handler = getattr(lane, 'onMsg' + msg['type'])
        handler(**msg)

class Resources:

    @classmethod
    def initialize(cls):
        for light in ('off', 'red', 'yellow', 'green'):
            pixmap = QtGui.QPixmap(':/console/icons/lights_%s.svg' % light)
            setattr(cls, light, pixmap)

        cls.tile = QtGui.QPixmap(':/console/icons/tile.png')
        cls.padlock = QtGui.QPixmap(':/console/icons/padlock.svg')
        cls.nopicture = QtGui.QPixmap(':/console/icons/nopicture.svg')
        cls.car = QtGui.QPixmap(':/console/icons/car.png')
        cls.empty = QtGui.QPixmap(1, 1)
        cls.empty.fill(QtCore.Qt.transparent)
        cls.icon = QtGui.QIcon()
        cls.icon.addPixmap(cls.padlock, QtGui.QIcon.Normal, QtGui.QIcon.Off)

class Configs:

    CR = u'\n'
    APPNAME = u'igate-console'

    @classmethod
    def initialize(cls, toplevel):

        defaults = {    'listenport'    : '3001',
                        'watchdog'      : '10',
                        'cleanup'       : '15',
                        'loglines'      : '100',
                        'fullscreen'    : 'false',
                        'style'         : 'pastique'
                   }

        c = ConfigParser()
        c.read(os.path.join(toplevel, 'console.ini'))

        def getOption(option):
            return c.get('console', option) if c.has_option('console', option) else defaults[option]

        cls.style = getOption('style')
        cls.cleanup = int(getOption('cleanup'))
        cls.loglines = int(getOption('loglines'))
        cls.watchdog = int(getOption('watchdog'))
        cls.fullscreen = getOption('fullscreen').lower() == 'true'
        cls.listenport = int(getOption('listenport'))

def showConsole(toplevel):
    app = QtGui.QApplication(sys.argv)
    Resources.initialize()
    Configs.initialize(toplevel)
    translator = QtCore.QTranslator()
    translator.load(os.path.join(toplevel, 'console_it'))
    app.installTranslator(translator)
    win = Console()
    win.show()
    return app.exec_()

def showConsoleDebug(toplevel):
    import time
    app = QtGui.QApplication(sys.argv)
    Resources.initialize()
    Configs.initialize(toplevel)
    translator = QtCore.QTranslator()
    translator.load(os.path.join(toplevel, 'console_it'))
    app.installTranslator(translator)
    messages = [{'permission_key' : '1234', 'permission':{
         'ownertype_id'          : 'PEOPLE',
         'auth'                  : 'REJECT',
         'auth_message'          : 'Autorizato',
         'permissiontype_name'   : 'Annuale',
         'people_id'             : None,
         'people_fullname'       : 'Mario Rossi',
         'people_birthday_date'  : '12-01-1983',
         'people_birthday_place' : 'La Spezia',
         'company_fullname'      : 'Infoporto La Spezia Srl 12345678910ABCDEFGHI',
         'company_city'          : 'La Spezia',
         'vip'                   : True
       }}, {'permission_key' : '12345', 'permission':{
        'uid_code'               : 'iioeoe',
         'auth'                  : 'REJECT',
         'auth_message'          : 'Badge Scaduto',
         'ownertype_id'          : 'VEHICLE',
         'permissiontype_name'   : 'Giornaliero',
         'people_id'             : None,
         'people_fullname'       : 'Gianni Verdi',
         'people_birthday_date'  : '20-01-1983',
         'people_birthday_place' : 'La Spezia',
         'company_fullname'      : 'Infoporto',
         'company_city'          : 'La Spezia',
         'vip'                   : False
       }},
       {'transitdirection_name' : 'Entrata' },
       {'transitdirection_name' : 'Uscita' }
    ]

    win = Console()
    win.show()
    lane1 = win.addLane('one', 1, [ ])
    lane2 = win.addLane('two', 2, ['COMPACT' ])
    lane3 = win.addLane('three', 4, ['COMPACT' ])
    lane4 = win.addLane('four', 3, ['COMPACT' ])
    lane1.imageurl = QtCore.QUrl('http://igate-img.gm.porto.laspezia.priv/')
    lane2.imageurl = QtCore.QUrl('http://igate-img.gm.porto.laspezia.priv/')
    lane3.imageurl = QtCore.QUrl('http://igate-img.gm.porto.laspezia.priv/')
    lane4.imageurl = QtCore.QUrl('http://igate-img.gm.porto.laspezia.priv/')

    lane1.setReady()
    lane1.onMsgAddPermission(**(messages[1]))
    lane2.onMsgAddPermission(**(messages[0]))
    lane3.onMsgAddPermission(**(messages[1]))
    lane1.onMsgAddPermission(**(messages[0]))
    lane4.onMsgAddPermission(**(messages[0]))
    lane1.onMsgSetTransitDirection(**(messages[2]))
    lane1.onMsgSetTransitDirection(**(messages[3]))
    lane2.onMsgSetTransitDirection(**(messages[2]))
    lane3.onMsgSetTransitDirection(**(messages[3]))
    attch = {'attachment_id':None, 'permission_key':'1234'}
    # lane2.onMsgAddPermissionAttachment(**attch)
    # lane1.onMsgAddPermissionAttachment(**attch)
    # lane.clearPermission()
    # lane.onMsgStartTransit()
    return app.exec_()

if __name__ == '__main__':
    base = os.path.abspath(__file__)
    toplevel = os.path.dirname(base)
    sys.exit(showConsole(toplevel))
