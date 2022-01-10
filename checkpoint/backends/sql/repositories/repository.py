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
import pickle
from twisted.internet.defer import inlineCallbacks, returnValue
from backends.base.repositories import RepositoryBase


class SQLRepository(RepositoryBase):
    repository_filename = None

    def __init__(self, backend):
        super(SQLRepository, self).__init__(backend)
        self.log = backend.log
        self.vacuum_counter = 0
        self.vacuum_threshold = backend.config['vacuum_threshold']
        assert self.repository_filename, 'invalid repository filename'
        self.connection = self.backend.get_connection(self.repository_filename)

    @inlineCallbacks
    def run_interaction(self, interaction, *args, **kwargs):
        result = yield self.connection.runInteraction(interaction, *args, **kwargs)
        returnValue(result)

    def vacuum(self, tx):
        if self.vacuum_threshold:
            self.vacuum_counter = (self.vacuum_counter + 1) % self.vacuum_threshold
            if self.vacuum_counter == 0:
                self.log.info('vacuum database...')
                tx.execute("VACUUM")

    def load_item(self, data):
        self.log.debug('loading data...')
        return pickle.loads(data.encode('latin1'))

    def dump_item(self, obj):
        self.log.debug('dumping object...')
        try:
            return pickle.dumps(obj).decode('latin1')
        except TypeError:
            self.log.failure('dumping object...')
            raise

