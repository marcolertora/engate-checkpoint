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

from repository import RepositoryBase


class DownloaderRepository(RepositoryBase):

    def update_item_repository(self, tx, repository_id, serial, signature):
        raise NotImplementedError

    def reset_item_repository(self, tx, repository_id, local_schema, remote_schema):
        raise NotImplementedError

    def get_item_repository(self, repository_id):
        raise NotImplementedError

    def insert_item(self, tx, repository_id, item_id, item_class, serial, signature, item, indexes):
        raise NotImplementedError

    def delete_item(self, tx, repository_id, item_id, item_class):
        raise NotImplementedError

    def get_item(self, tx, repository_id, item_id, item_class):
        raise NotImplementedError

    def get_items_signatures(self, tx, repository_id):
        raise NotImplementedError

    def get_item_by_index(self, tx, repository_id, item_class, key, value):
        raise NotImplementedError
