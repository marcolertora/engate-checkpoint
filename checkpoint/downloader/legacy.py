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
from twisted.web.xmlrpc import Proxy
from backends import ItemNotFound
from configuration import val
from twisted.internet.defer import inlineCallbacks, returnValue
from base import DownloaderBase
from helpers import patch_xmlrpclib, XMLRPCExceptions
from repository import Repository

patch_xmlrpclib()


class DownloaderLegacy(DownloaderBase):

    CONFIG_SCHEMA = DownloaderBase.CONFIG_SCHEMA.extend({
        vol.Required('url'): vol.Url(),
        vol.Optional('username', default=None): vol.Maybe(str),
        vol.Optional('password', default=None): vol.Maybe(str),
        vol.Required('http_timeout', default=20): val.timeout,
        vol.Required('repositories'): {str: Repository.CONFIG_SCHEMA},
    })

    __slots__ = DownloaderBase.__slots__ + ['endpoint', 'repositories']

    def __init__(self, config, checkpoint):
        super(DownloaderLegacy, self).__init__(config, checkpoint)
        self.repositories = dict()
        self.endpoint = Proxy(config['url'],
                              connectTimeout=config['http_timeout'],
                              user=config['username'],
                              password=config['password'],
                              allowNone=True,
                              useDateTime=True)
        self.endpoint.queryFactory.noisy = False

        for repository_id, repository_config in config['repositories'].items():
            self.log.info('add new repository {repository}...', repository=repository_id)
            self.repositories[repository_id] = Repository(repository_id, repository_config, self)

    @property
    def backend(self):
        return self.checkpoint.backend.downloader

    def starting(self):
        for repository in self.repositories.values():
            repository.start()

    @inlineCallbacks
    def get_credential(self, repository_id, credential_code):
        owner = yield self.backend.run_interaction(self.backend.get_item_by_index,
                                                   repository_id,
                                                   Repository.ITEM_CLASS.OWNER,
                                                   Repository.INDEX_KEY.CREDENTIAL_CODE,
                                                   credential_code)
        credential = owner.get_credential(credential_code)
        assert credential, 'credential should exist'
        returnValue(credential)

    @inlineCallbacks
    def get_credential_remote(self, credential_code):
        self.log.info('requesting credential to legacy remote...')
        try:
            result = yield self.endpoint.callRemote('PeopleService.fullPeopleByBadgeCode', credential_code)
        except XMLRPCExceptions, err:
            self.log.error('request: {err}', err=err)
            raise ItemNotFound('item not found on remote')

        if not result:
            raise ItemNotFound('item not found on remote')

        owner = Repository.load_item_data(Repository.ITEM_CLASS.OWNER, result)
        credential = owner.get_credential(credential_code)
        assert credential, 'credential should exist'
        returnValue(credential)

    @inlineCallbacks
    def get_photo(self, repository_id, photo_id):
        item = yield self.backend.run_interaction(self.backend.get_item,
                                                  repository_id,
                                                  photo_id,
                                                  Repository.ITEM_CLASS.PHOTO)
        returnValue(item)

    @inlineCallbacks
    def get_photo_remote(self, photo_id):
        raise NotImplementedError
