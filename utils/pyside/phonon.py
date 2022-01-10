#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of the PySide project.
#
# Copyright (C) 2010 Nokia Corporation and/or its subsidiary(-ies).
#
# Contact: PySide team <contact@pyside.org>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public License
# version 2.1 as published by the Free Software Foundation. Please
# review the following information to ensure the GNU Lesser General
# Public License version 2.1 requirements will be met:
# http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html.
# #
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA
# 02110-1301 USA


import sys
from PySide import QtGui, QtCore
from PySide.phonon import Phonon

class iPlayer(QtGui.QDialog):

    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)

        self.medias = list()

        self.showFullScreen()
        self.setCursor(QtCore.Qt.BlankCursor)
        self.setWindowFlags(QtCore.Qt.WindowTitleHint | QtCore.Qt.FramelessWindowHint)

        mainLayout = QtGui.QVBoxLayout(self)

        self.gridLayout = QtGui.QGridLayout()
        mainLayout.addLayout(self.gridLayout)

        button = QtGui.QPushButton('Exit')
        button.clicked.connect(app.exit)
        mainLayout.addWidget(button)

        self.setLayout(mainLayout)

    def addMediaPlayer(self, index, url):
        player = Phonon.VideoWidget()
        media = Phonon.MediaObject()
        media.setCurrentSource(Phonon.MediaSource(url))
        Phonon.createPath(media, player)
        Phonon.createPath(media, Phonon.AudioOutput(Phonon.VideoCategory))
        x, y = divmod(index, 2)
        self.gridLayout.addWidget(player, x, y)
        self.medias.append(media)
        media.play()


if __name__ == '__main__':

    # rtsp demo
    #url = 'rtsp://184.72.239.149/vod/mp4:BigBuckBunny_115k.mov'
    # http demo
    #url = 'http://184.72.239.149/vod/mp4:BigBuckBunny_115k.mov'
    # http mjpg ()
    #url = 'http://root:root@172.16.20.20/mjpg/video.mjpg'
    # rtsp mpg4 (old axis)
    #url = 'rtsp://root:root@172.16.20.20/mpeg4/media.amp'
    # rtsp mpg4 (new axis)
    url = 'rtsp://root:root@172.16.1.145/axis-media/media.amp'

    app = QtGui.QApplication(sys.argv)
    app.setApplicationName('Demo')

    win = iPlayer()

    for index in range(4):
        win.addMediaPlayer(index, url)

    win.show()
    app.exec_()
