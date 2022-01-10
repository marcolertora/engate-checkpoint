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

import voluptuous as vol
from backends import ItemNotFound
from twisted.internet.defer import inlineCallbacks, returnValue
from base import DownloaderBase
from legacy import DownloaderLegacy
from engate import DownloaderEnGate


class DownloaderMixed(DownloaderBase):

    CONFIG_SCHEMA = DownloaderBase.CONFIG_SCHEMA.extend({
        vol.Required('legacy'): DownloaderLegacy.CONFIG_SCHEMA,
        vol.Required('engate'): DownloaderEnGate.CONFIG_SCHEMA,
        vol.Required('fallback_on_remote', default=False): bool,
    })

    __slots__ = DownloaderBase.__slots__ + ['legacy', 'engate', 'fallback_on_remote']

    def __init__(self, config, checkpoint):
        super(DownloaderMixed, self).__init__(config, checkpoint)
        self.legacy = DownloaderLegacy(config['legacy'], checkpoint)
        self.engate = DownloaderEnGate(config['engate'], checkpoint)
        self.fallback_on_remote = config['fallback_on_remote']

    @property
    def backend(self):
        return self.checkpoint.backend.downloader

    def starting(self):
        pass

    @inlineCallbacks
    def get_credential(self, repository_id, credential_code):
        lookup_functions = [self.engate.get_credential_remote, self.legacy.get_credential_remote]
        for lookup_function in lookup_functions:
            try:
                credential = yield lookup_function(credential_code)
            except ItemNotFound:
                self.log.warn('item not found, try next')
            else:
                returnValue(credential)

        raise ItemNotFound('item not found')

    @inlineCallbacks
    def get_photo(self, repository_id, photo_id):
        photo = yield self.engate.get_photo_remote(photo_id)
        returnValue(photo)
