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


class SQLItemRepository(object):

    __slots__ = ['repository_id', 'local_schema', 'remote_schema', 'signature', 'serial']

    def __init__(self, repository_id, local_schema, remote_schema, signature=None, serial=0):
        self.repository_id = repository_id
        self.local_schema = local_schema
        self.remote_schema = remote_schema
        self.signature = signature
        self.serial = serial

    @staticmethod
    def create(tx):
        template = """
            CREATE TABLE IF NOT EXISTS items_repositories (
            repository_id VARCHAR(16),
            local_schema INTEGER, 
            remote_schema INTEGER, 
            signature VARCHAR(32), 
            serial INTEGER, 
            PRIMARY KEY(repository_id))
        """
        tx.execute(template)

    @staticmethod
    def get(tx, repository_id):
        params = dict(repository_id=repository_id)
        template = """
            SELECT repository_id, local_schema, remote_schema, signature, serial 
            FROM items_repositories 
            WHERE repository_id = :repository_id
        """
        tx.execute(template, params)
        result = tx.fetchone()
        if result is not None:
            return SQLItemRepository(*result)

    @staticmethod
    def insert(tx, repository):
        params = dict(repository_id=repository.repository_id,
                      local_schema=repository.local_schema,
                      remote_schema=repository.remote_schema,
                      serial=repository.serial,
                      signature=repository.signature)
        template = """
            INSERT INTO items_repositories (
            repository_id, local_schema, remote_schema, serial, signature
            ) VALUES (
            :repository_id, :local_schema, :remote_schema, :serial, :signature
            )
        """
        tx.execute(template, params)

    @staticmethod
    def delete(tx, repository_id):
        params = dict(repository_id=repository_id)
        template = """
            DELETE FROM items_repositories 
            WHERE repository_id = :repository_id
        """
        tx.execute(template, params)

    @staticmethod
    def update(tx, repository_id, serial, signature):
        params = dict(repository_id=repository_id, serial=serial, signature=signature)
        template = """
            UPDATE items_repositories SET 
            serial = :serial,
            signature = :signature
            WHERE repository_id = :repository_id
        """
        tx.execute(template, params)
