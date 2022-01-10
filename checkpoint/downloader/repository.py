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
import binascii
import json
from argparse import Namespace
from collections import namedtuple
from datetime import timedelta, datetime
import voluptuous as vol
from configuration import val
from twisted.internet.defer import inlineCallbacks
from hashlib import md5
from exceptions import DownloaderException
from legacy_mapper import map_user, map_photo, map_owner
from commons.owners import Owner
from helpers import class_repr, class_str, XMLRPCExceptions, LoopInteraction, LoopShouldWait

Index = namedtuple('Index', ['key', 'value'])


class Repository(object):

    CONFIG_SCHEMA = vol.Schema({
        vol.Required('interval', default=60.0): val.interval,
        vol.Required('limit_min_threshold', default=500): vol.All(int, vol.Range(min=1)),
        vol.Required('limit_max_threshold', default=5000): vol.All(int, vol.Range(min=1, max=10000)),
    })

    SCHEMA_VERSION = 1
    ITEM_REMOVED = 'REMOVED'

    OPERATION = Namespace(UPDATE='UPDATE',
                          RESET='RESET',
                          DUNNO='DUNNO')

    ITEM_CLASS = Namespace(OWNER='PEOPLE',
                           PHOTO='PHOTO',
                           USER='USER')

    INDEX_KEY = Namespace(CREDENTIAL_CODE='CREDENTIAL_CODE',
                          CREDENTIAL_PIN_CODE='CREDENTIAL_PIN_CODE')

    __slots__ = ['repository_id', 'manager', 'loop']

    log = Logger()

    def __init__(self, repository_id, config, manager):
        self.repository_id = repository_id
        self.manager = manager
        self.loop = LoopInteraction(initialize=self.manager.backend.initialize,
                                    interaction=lambda: self.manager.backend.run_interaction(self.interaction),
                                    interval=config['interval'],
                                    limit_min_threshold=config['limit_min_threshold'],
                                    limit_max_threshold=config['limit_max_threshold'])

    def __repr__(self):
        return class_repr(self, self.repository_id)

    def __str__(self):
        return class_str(self, self.repository_id)

    def start(self):
        self.loop.start()

    @inlineCallbacks
    def interaction(self, limit):
        self.log.debug('synchronizing limit {limit}...')
        local_repository = yield self.manager.backend.get_item_repository(self.repository_id)

        if not local_repository:
            self.log.info('no repository found in backend')
            yield self.manager.backend.run_interaction(self.reset)
            return

        if local_repository.local_schema != self.SCHEMA_VERSION:
            self.log.info('backend repository local schema mismatch')
            yield self.manager.backend.run_interaction(self.reset)
            return

        self.log.debug('request sync version {version} serial {serial} signature {signature}',
                       version=local_repository.remote_schema,
                       serial=local_repository.serial,
                       signature=local_repository.signature)

        try:
            result = yield self.manager.endpoint.callRemote('OfflineSyncService.sync',
                                                            self.repository_id,
                                                            local_repository.remote_schema,
                                                            local_repository.serial,
                                                            local_repository.signature,
                                                            limit)
        except XMLRPCExceptions, err:
            self.log.error('request: {err}', err=err)
            raise LoopShouldWait()

        yield self.manager.backend.run_interaction(self.handle_result, result)

    def handle_result(self, tx, result):
        self.log.debug('operation {operation} {count} items', operation=result['operation'], count=len(result['items']))

        if result['operation'] == Repository.OPERATION.UPDATE:
            self.log.info('{count} items to update', count=len(result['items']))
            self.update(tx, result['items'])

        elif result['operation'] == Repository.OPERATION.RESET:
            # the remote said to reset. signature / version mismatch
            self.log.info('reset requested, reason {reason}', reason=result['message'])
            self.log.info('{count} items to update', count=len(result['items']))
            self.reset(tx, result['version'])
            self.update(tx, result['items'])

        elif result['operation'] == Repository.OPERATION.DUNNO:
            self.log.debug('updated, nothing to do')
            raise LoopShouldWait()

        else:
            raise DownloaderException('operation {operation} unknown'.format(operation=result['operation']))

    def update_items(self, tx, items):
        for item in items:
            self.manager.backend.delete_item(tx,
                                             self.repository_id,
                                             item['itemId'],
                                             item['itemClass'])

            if item['itemData'] != Repository.ITEM_REMOVED:
                item_object = Repository.parse_item_data(item['itemClass'], item['itemData'])
                item_indexes = Repository.extract_indexes(item_object)
                self.manager.backend.insert_item(tx,
                                                 self.repository_id,
                                                 item['itemId'],
                                                 item['itemClass'],
                                                 item['itemSerial'],
                                                 item['itemSignature'],
                                                 item_object,
                                                 item_indexes)

    def calculate_signature(self, tx):
        """
        calculate the full repository signature.
        the signature is the hex md5 of all the item signatures ordered by item_class ASC, serial ASC
        """
        signatures = self.manager.backend.get_items_signatures(tx, self.repository_id)
        return md5(''.join(signatures)).hexdigest().upper()

    def update(self, tx, items):
        if len(items):
            self.log.info('updating {count} items...', count=len(items))
            self.update_items(tx, items)
            serial = max([item['itemSerial'] for item in items])
            signature = self.calculate_signature(tx)
            self.manager.backend.update_item_repository(tx, self.repository_id, serial, signature)

    def reset(self, tx, remote_version=None):
        self.log.info('resetting repository...')
        self.manager.backend.reset_item_repository(tx, self.repository_id, self.SCHEMA_VERSION, remote_version)

    @staticmethod
    def extract_indexes(item_object):
        indexes = list()

        if isinstance(item_object, Owner):
            for credential in item_object.credentials:
                if credential.code:
                    indexes.append(Index(Repository.INDEX_KEY.CREDENTIAL_CODE, credential.code))

                if credential.pin_code:
                    indexes.append(Index(Repository.INDEX_KEY.CREDENTIAL_PIN_CODE, credential.pin_code))

            return indexes

        return indexes

    @staticmethod
    def parse_item_data(item_class, item_data):
        item_dict = json.loads(item_data, object_hook=Repository.legacy_json_object_hook)
        return Repository.load_item_data(item_class, item_dict)

    @staticmethod
    def load_item_data(item_class, item_dict):

        if item_class == Repository.ITEM_CLASS.OWNER:
            return map_owner(item_dict)

        if item_class == Repository.ITEM_CLASS.USER:
            return map_user(item_dict)

        if item_class == Repository.ITEM_CLASS.PHOTO:
            return map_photo(item_dict)

        raise NotImplementedError('unknown item class {0}'.format(item_class))

    @staticmethod
    def legacy_json_object_hook(data):
        assert isinstance(data, dict), 'invalid data type'

        for key, value in data.items():

            if not isinstance(value, (str, unicode)):
                continue

            if value.startswith('@date:'):
                try:
                    data[key] = datetime.fromtimestamp(0) + timedelta(milliseconds=int(value[len('@date:'):]))
                except ValueError:
                    data[key] = None

            elif value.startswith('@binary:'):
                try:
                    data[key] = value[len('@binary:'):].decode('base64')
                except binascii.Error:
                    data[key] = None

        return data
