# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'console.ui'
#
# Created: Thu Apr 26 18:32:16 2012
#      by: pyside-uic 0.2.13 running on PySide 1.1.1
#
# WARNING! All changes made in this file will be lost!

import console_rc
from PySide import QtCore, QtGui

class Ui_Lane(object):

    def setupUi(self, Lane):
        self.lane = Lane
        Lane.setObjectName("Lane")
        self.setLaneSize()

        # layout esterno
        self.layout = QtGui.QGridLayout(Lane)
        self.layout.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.layout.setObjectName("layout")

        # layout che contiene i widget
        self.mainLayout = QtGui.QVBoxLayout()
        self.mainLayout.setObjectName("mainLayout")
        # setContentsMargins(left, top, right, bottom)

        # layout status
        self.statusLayout = QtGui.QHBoxLayout()
        self.statusLayout.setContentsMargins(-1, -1, -1, 0)
        self.statusLayout.setObjectName("statusLayout")

        self.qlLaneInfo = QtGui.QLabel(Lane)
        self.qlLaneInfo.setText("")
        self.qlLaneInfo.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.qlLaneInfo.setObjectName("qlLaneInfo")
        self.statusLayout.addWidget(self.qlLaneInfo)

        self.qlStatusImage = QtGui.QLabel(Lane)
        self.qlStatusImage.setMinimumSize(QtCore.QSize(80, 80))
        self.qlStatusImage.setMaximumSize(QtCore.QSize(80, 80))
        self.qlStatusImage.setStyleSheet("")
        self.qlStatusImage.setText("")
        self.qlStatusImage.setScaledContents(True)
        self.qlStatusImage.setAlignment(QtCore.Qt.AlignCenter)
        self.qlStatusImage.setObjectName("qlStatusImage")
        self.statusLayout.addWidget(self.qlStatusImage)

        self.mainLayout.addLayout(self.statusLayout)

        self.qlStatus = QtGui.QLabel(Lane)
        self.qlStatus.setMaximumSize(QtCore.QSize(16777215, 78))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setWeight(75)
        font.setBold(True)
        self.qlStatus.setFont(font)
        self.qlStatus.setStyleSheet("")
        self.qlStatus.setText("")
        self.qlStatus.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.qlStatus.setWordWrap(True)
        self.qlStatus.setObjectName("qlStatus")
        self.mainLayout.addWidget(self.qlStatus)

        # Button Toolbar
        self.buttonLayout = QtGui.QHBoxLayout()
        self.mainLayout.addLayout(self.buttonLayout)

        # Premissions Widget
        self.widgetItemList = dict()
        self.qlwPermissionList = QtGui.QListWidget(Lane)

        sizeW = 265 if self.lane.isCompact() else 280
        self.qlwPermissionList.setMinimumSize(QtCore.QSize(280, 205))

        self.qlwPermissionList.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.qlwPermissionList.setVerticalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
        self.qlwPermissionList.setSpacing(5)
        self.mainLayout.addWidget(self.qlwPermissionList)

        self.qlPlate = QtGui.QLabel(Lane)
        self.qlPlate.setStyleSheet("border: 1px solid black;")
        self.qlPlate.setText("")
        self.qlPlate.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.qlPlate.setMinimumSize(QtCore.QSize(0, 50))
        self.qlPlate.setMaximumSize(QtCore.QSize(16777215, 50))
        self.qlPlate.setObjectName("qlPlate")
        self.mainLayout.addWidget(self.qlPlate)

        self.qteLog = QtGui.QTextEdit(Lane)
        self.qteLog.setAcceptDrops(False)
        self.qteLog.setStyleSheet("background-color:transparent;border: 1px solid black;")
        self.qteLog.setFrameShadow(QtGui.QFrame.Sunken)
        self.qteLog.setLineWidth(1)
        self.qteLog.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.qteLog.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.qteLog.setUndoRedoEnabled(False)
        self.qteLog.setReadOnly(True)
        self.qteLog.setAcceptRichText(True)
        self.qteLog.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.qteLog.setObjectName("qteLog")
        self.qteLog.setMinimumSize(QtCore.QSize(0, 0))
        self.qteLog.setMaximumSize(QtCore.QSize(16777215, 100))

        self.mainLayout.addWidget(self.qteLog)
        self.layout.addLayout(self.mainLayout, 1, 0, 1, 1)
        self.retranslateUi(Lane)
        QtCore.QMetaObject.connectSlotsByName(Lane)

    def addPermissionWidget(self, permission_key, permission, picture, transitinfo):
        qpermission = UI_Permission(permission, picture, transitinfo)
        item = QtGui.QListWidgetItem()
        item.setSizeHint(qpermission.size())
        self.qlwPermissionList.addItem(item)
        self.qlwPermissionList.setItemWidget(item, qpermission)
        self.widgetItemList[permission_key] = (qpermission, item)

    def addImagePermissionWidget(self, permission_key, picture):
        qwid, item = self.widgetItemList.get(permission_key)
        if not qwid is None:
            qwid.setBiometricImage(picture)
            item.setSizeHint(qwid.size())

    def updateDirectionPermissionWidget(self, transitinfo):
        direction = transitinfo['transitdirection_name']
        for qwid, item in self.widgetItemList.values():            
            if not qwid is None: qwid.setDirection(direction)
            
    def clearPermissionList(self):
        self.qlwPermissionList.clear()
        self.widgetItemList = dict()

    def setLaneSize(self):
        # Lane.resize(260, 900)
        height = 700 if self.isCompact() else 16777215
        width = 285 if self.isCompact() else 300
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lane.sizePolicy().hasHeightForWidth())
        self.lane.setSizePolicy(sizePolicy)
        self.lane.setMinimumSize(QtCore.QSize(0, 0))
        self.lane.setMaximumSize(QtCore.QSize(300, height))
        # self.lane.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.lane.setFlat(False)
        self.lane.setCheckable(False)

    def retranslateUi(self, Lane):
        Lane.setWindowTitle(QtGui.QApplication.translate("Lane", "Form", None, QtGui.QApplication.UnicodeUTF8))
        Lane.setTitle(QtGui.QApplication.translate("Lane", "Corsia", None, QtGui.QApplication.UnicodeUTF8))

class UI_Permission(QtGui.QWidget):

    def __init__(self, permission, picture, transitinfo, parent=None):
        super(UI_Permission, self).__init__(parent)
        self.imageSizeX = 58
        self.imageSizeY = 80
        self.sizeX = 250
        self.sizeY = 90
        self.textLabelX = 170
        self.textLabelXB = 250
        self.textLabelY = 15
        self.authImageX = 5
        self.authImageY = self.imageSizeX
        self.spacing = 5
        self.initUI(permission, picture, transitinfo)

    def initUI(self, permission, picture, transitinfo):
        # self.setStyleSheet("background-color:transparent;border: 1px solid black;")
        self.borderWidget = QtGui.QFrame(self)
        self.borderWidget.setStyleSheet("background-color: #9c9c9c;border: 1px solid black;")

        self.qlPhoto = QtGui.QLabel(self)
        self.qlPhoto.setMinimumSize(QtCore.QSize(self.imageSizeX, self.imageSizeY))
        self.qlPhoto.setMaximumSize(QtCore.QSize(self.imageSizeX, self.imageSizeY))
        self.qlPhoto.setStyleSheet("border: 1px solid black;background-color: white;")
        self.qlPhoto.setText("")
        self.qlPhoto.setGeometry(QtCore.QRect(5, 5, self.imageSizeX, self.imageSizeY))
        self.qlPhoto.setPixmap(QtGui.QPixmap(picture.scaled(self.qlPhoto.size(), QtCore.Qt.KeepAspectRatio)))

        labelAlignX1 = self.imageSizeX + 2 * self.spacing
        labelAlignX2 = labelAlignX1 + (self.sizeX - labelAlignX1) / 2 + self.spacing
        
        # name label
        self.qlPeopleFullname = QtGui.QLabel(self)
        self.qlPeopleFullname.setText(permission['people_fullname'])
        self.qlPeopleFullname.setStyleSheet('font: bold 9pt "Arial";')
        self.qlPeopleFullname.setGeometry(QtCore.QRect(labelAlignX1, 5, self.textLabelX, self.textLabelY))

        # agency label
        self.qlCompanyFullname = QtGui.QLabel(self)
        self.qlCompanyFullname.setText(permission['company_fullname'])
        self.qlCompanyFullname.setGeometry(QtCore.QRect(labelAlignX1, 20, self.textLabelX, self.textLabelY))

        
        # direction
        self.qlDirection = QtGui.QLabel(self)
        if transitinfo.has_key('transitdirection_name'): self.qlDirection.setText(transitinfo['transitdirection_name'])
        self.qlDirection.setStyleSheet('font: bold 10pt "Arial";')       
        self.qlDirection.setGeometry(QtCore.QRect(labelAlignX1, 55, self.textLabelX, self.textLabelY))
        
        # VIP
        self.qlVip = QtGui.QLabel(self)
        self.qlVip.setText("VIP")
        self.qlVip.setGeometry(QtCore.QRect(labelAlignX2, 55, self.textLabelX, self.textLabelY))
        self.qlVip.setStyleSheet('font: bold 10pt "Arial";')
        vip = permission.get('vip') if permission.get('vip') is not None else False
        self.qlVip.setVisible(vip)

        # permission type
        self.qlPermissionType = QtGui.QLabel(self)
        self.qlPermissionType.setText(permission['permissiontype_name'])
        self.qlPermissionType.setGeometry(QtCore.QRect(labelAlignX1, 70, self.textLabelX, self.textLabelY))
        
        # esito
        authenticated = permission['auth'] in ('ALLOW', 'OPERATOR', 'BIOMETRIC')
        self.qlAuthenticationMessage = QtGui.QLabel(self)
        self.qlAuthenticationMessage.setText(permission['auth_message'])
        self.qlAuthenticationMessage.setGeometry(QtCore.QRect(self.spacing, 87, self.sizeX, self.textLabelY))
        self.qlAuthenticationMessage.setVisible(not authenticated)
        self.qlAuthenticationMessage.setStyleSheet("font: bold; color: #ff0000;")
        if not authenticated: self.sizeY = self.sizeY + self.textLabelY

        # semaforo
        self.qlAuthenticationLabel = QtGui.QLabel(self)
        self.qlAuthenticationLabel.setText("")
        self.qlAuthenticationLabel.setGeometry(QtCore.QRect(self.sizeX - (self.spacing * 2), self.spacing, self.authImageX, self.authImageY))
        self.qlAuthenticationLabel.setStyleSheet("background-color: %s;" % ('#00d900' if authenticated else '#ff0000'))

        self.qlBiometricImage = QtGui.QLabel(self)
        self.qlBiometricImage = QtGui.QLabel(self)
        self.qlBiometricImage.setMinimumSize(QtCore.QSize(self.imageSizeX, self.imageSizeY))
        self.qlBiometricImage.setMaximumSize(QtCore.QSize(self.imageSizeX, self.imageSizeY))
        self.qlBiometricImage.setStyleSheet("border: 1px solid black;background-color: white;")
        self.qlBiometricImage.setText("")
        self.qlBiometricImage.setGeometry(QtCore.QRect(5, (self.sizeY), self.imageSizeX, self.imageSizeY))
        self.qlBiometricImage.setVisible(False)

        # dimensioni
        self.setFixedSize(self.sizeX, self.sizeY)
        self.borderWidget.setGeometry(QtCore.QRect(0, 0, self.size().width(), self.size().height()))

    def setDirection(self, direction):
        self.qlDirection.setText(direction)
        
    def setBiometricImage(self, picture):
        height = self.size().height() + self.qlBiometricImage.size().height() + self.spacing
        self.setFixedSize(self.sizeX, height)
        self.borderWidget.setGeometry(QtCore.QRect(0, 0, self.size().width(), self.size().height()))
        self.qlBiometricImage.setPixmap(QtGui.QPixmap(picture.scaled(self.qlPhoto.size(), QtCore.Qt.KeepAspectRatio)))
        self.qlBiometricImage.setVisible(True)
