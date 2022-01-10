#!/usr/bin/env python
# -*- Mode: Python; tab-width: 4 -*-
#
# engate-checkpoint
#
# Copyright (C) 2018 Marco Lertora <marco.lertora@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from twisted.logger import Logger
from repositories import UploaderRepository, DownloaderRepository
from helpers import class_repr, class_str


class BackendBase(object):

    log = Logger()
    uploader_factory = UploaderRepository
    downloader_factory = DownloaderRepository

    __slots__ = ['config', 'uploader', 'downloader']

    def __init__(self, config):
        assert isinstance(config, dict), 'invalid config'
        self.config = config
        assert issubclass(self.uploader_factory, UploaderRepository)
        self.uploader = self.uploader_factory(self)
        assert issubclass(self.downloader_factory, DownloaderRepository)
        self.downloader = self.downloader_factory(self)

    def __repr__(self):
        return class_repr(self)

    def __str__(self):
        return class_str(self)

