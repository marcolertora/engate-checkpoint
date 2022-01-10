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
from twisted.internet.defer import inlineCallbacks, returnValue
from backends.base import ItemNotFound
from backends.base.repositories import DownloaderRepository
from sql_item import SQLItem
from sql_item_repository import SQLItemRepository
from repository import SQLRepository


class DownloaderSQLRepository(DownloaderRepository, SQLRepository):
    repository_filename = 'database_downloader'

    @inlineCallbacks
    def initialize(self):
        self.log.debug('initialize database...')
        yield self.run_interaction(SQLItemRepository.create)

    def update_item_repository(self, tx, repository_id, serial, signature):
        self.log.info('update item repository {repository}...', repository=repository_id)
        SQLItemRepository.update(tx, repository_id, serial, signature)

    def reset_item_repository(self, tx, repository_id, local_schema, remote_schema):
        self.log.info('reset item repository {repository}...', repository=repository_id)
        SQLItem.drop(tx, repository_id)
        SQLItem.create(tx, repository_id)
        SQLItemRepository.delete(tx, repository_id)
        SQLItemRepository.insert(tx, SQLItemRepository(repository_id, local_schema, remote_schema))

    @inlineCallbacks
    def get_item_repository(self, repository_id):
        self.log.debug('retrieve item repository {repository}...', repository=repository_id)
        result = yield self.run_interaction(SQLItemRepository.get, repository_id)
        returnValue(result)

    def insert_item(self, tx, repository_id, item_id, item_class, serial, signature, item, indexes):
        self.log.debug('insert item in repository {repository}...', repository=repository_id)
        item = SQLItem(item_id, item_class, signature, serial, self.dump_item(item))
        SQLItem.insert(tx, repository_id, item, indexes)

    def delete_item(self, tx, repository_id, item_id, item_class):
        SQLItem.delete(tx, repository_id, item_id, item_class)
        self.vacuum(tx)

    def get_item(self, tx, repository_id, item_id, item_class):
        self.log.debug('retrieve items in repository {repository}...', repository=repository_id)
        item = SQLItem.get(tx, repository_id, item_id, item_class)
        if not item:
            raise ItemNotFound('no item {0} found!'.format(item_class))
        return self.load_item(item.data)

    def get_items_signatures(self, tx, repository_id):
        self.log.debug('retrieve items signatures in repository {repository}...', repository=repository_id)
        return SQLItem.get_signatures(tx, repository_id)

    def get_item_by_index(self, tx, repository_id, item_class, key, value):
        self.log.debug('retrieve items in repository {repository}...', repository=repository_id)
        items = SQLItem.get_by_index(tx, repository_id, item_class, key, value)
        if len(items) < 1:
            raise ItemNotFound('no item {0} found!'.format(item_class))
        if len(items) > 1:
            raise ItemNotFound('too many items {0} found!'.format(item_class))

        return self.load_item(items[0].data)
