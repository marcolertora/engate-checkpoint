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
import voluptuous as vol
from twisted.internet.defer import inlineCallbacks
from helpers import class_repr, class_str


class DownloaderBase(object):

    __slots__ = ['checkpoint', 'disabled']

    log = Logger()

    CONFIG_SCHEMA = vol.Schema({
        vol.Required('disabled', default=False): bool,
    })

    def __init__(self, config, checkpoint):
        assert config is not None, 'invalid config'
        self.checkpoint = checkpoint
        self.disabled = config['disabled']

    def __repr__(self):
        return class_repr(self)

    def __str__(self):
        return class_str(self)

    def start(self):
        if self.disabled:
            self.log.warn('is disabled, skip start')
            return

        self.log.info('starting...')
        self.starting()

    def starting(self):
        raise NotImplementedError

    @inlineCallbacks
    def get_photo(self, repository_id, photo_id):
        raise NotImplementedError

    @inlineCallbacks
    def get_credential(self, repository_id, credential_code):
        raise NotImplementedError
