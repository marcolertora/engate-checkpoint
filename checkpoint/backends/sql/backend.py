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

import os
from twisted.enterprise import adbapi
import voluptuous as vol
from backends.base import BackendBase
from repositories import UploaderSQLRepository, DownloaderSQLRepository
from twisted.logger import Logger


class BackendSQL(BackendBase):

    log = Logger()

    uploader_factory = UploaderSQLRepository
    downloader_factory = DownloaderSQLRepository

    __slots__ = BackendBase.__slots__ + ['vacuum_counter', 'vacuum_threshold']

    CONFIG_SCHEMA = vol.Schema({
        vol.Required('root_folder'): vol.IsDir(),
        vol.Required('vacuum_threshold', default=5000): vol.All(int, vol.Range(min=0)),
    })

    def get_connection(self, filename):
        filename = os.path.join(self.config['root_folder'], filename)
        self.log.info('loading database sqlite:{filename}...', filename=filename)
        return adbapi.ConnectionPool('sqlite3',
                                     filename,
                                     check_same_thread=False,
                                     cp_openfun=BackendSQL.on_connect)

    @staticmethod
    def on_connect(tx):
        query = 'PRAGMA foreign_keys = ON;'
        tx.execute(query)
        query = 'PRAGMA journal_mode = WAL;'
        tx.execute(query)
        query = 'PRAGMA busy_timeout = 10000;'
        tx.execute(query)

