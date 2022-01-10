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
from configuration import val
from twisted.internet.defer import inlineCallbacks, returnValue
from base import DownloaderBase
from downloader.engate_mapper import map_owner, map_photo
from helpers import JsonServerProxy, JSONRPCException


class DownloaderEnGate(DownloaderBase):

    CONFIG_SCHEMA = DownloaderBase.CONFIG_SCHEMA.extend({
        vol.Required('base_url'): vol.Url(),
        vol.Optional('username', default=None): vol.Maybe(str),
        vol.Optional('password', default=None): vol.Maybe(str),
        vol.Required('http_timeout', default=20): val.timeout
    })

    __slots__ = DownloaderBase.__slots__ + ['endpoint']

    def __init__(self, config, checkpoint):
        super(DownloaderEnGate, self).__init__(config, checkpoint)
        self.endpoint = JsonServerProxy(config['base_url'],
                                        config['username'],
                                        config['password'],
                                        config['http_timeout'])

    @property
    def backend(self):
        return self.checkpoint.backend.downloader

    def starting(self):
        pass

    @inlineCallbacks
    def get_credential(self, repository_id, credential_code):
        raise NotImplementedError

    @inlineCallbacks
    def get_credential_remote(self, credential_code):
        self.log.info('requesting credential to engate remote...')
        try:
            result = yield self.endpoint.get('/get_owner_by_credential/{code}'.format(code=credential_code))
        except JSONRPCException as err:
            raise ItemNotFound(err)

        assert result is not None, 'result should not be none'
        owner = map_owner(result['owner'])
        credential = owner.get_credential(credential_code)
        assert credential, 'credential should exist'
        returnValue(credential)

    @inlineCallbacks
    def get_photo(self, repository_id, photo_id):
        raise NotImplementedError

    @inlineCallbacks
    def get_photo_remote(self, photo_id):
        try:
            result = yield self.endpoint.get('/get_photo/{photo_id}'.format(photo_id=photo_id))
        except JSONRPCException as err:
            raise ItemNotFound(err)

        assert result is not None, 'result should not be none'
        item = map_photo(result['photo'])
        returnValue(item)
