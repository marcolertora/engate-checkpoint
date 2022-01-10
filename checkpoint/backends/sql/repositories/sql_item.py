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


class SQLItem(object):

    __slots__ = ['item_id', 'item_class', 'signature', 'serial', 'data']

    def __init__(self, item_id, item_class, signature, serial, data):
        self.item_id = item_id
        self.item_class = item_class
        self.signature = signature
        self.serial = serial
        self.data = data

    @staticmethod
    def create(tx, repository_id):
        table = SQLItem.get_table(repository_id)
        template = """
            CREATE TABLE IF NOT EXISTS {table} (
                item_id VARCHAR(16),
                item_class VARCHAR(16), 
                signature VARCHAR(32),
                serial INTEGER, 
                data VARCHAR,
                PRIMARY KEY(item_id, item_class))
        """
        tx.execute(template.format(table=table))

        template = """
            CREATE TABLE IF NOT EXISTS {table}_index (
                item_id VARCHAR(16),
                item_class VARCHAR(16), 
                key VARCHAR(16),
                value VARCHAR(64),
                FOREIGN KEY(item_id, item_class) 
                REFERENCES {table}(item_id, item_class) ON DELETE CASCADE)
        """
        tx.execute(template.format(table=table))

    @staticmethod
    def drop(tx, repository_id):
        table = SQLItem.get_table(repository_id)

        template = "DROP TABLE IF EXISTS {table}"
        tx.execute(template.format(table=table))

        template = "DROP TABLE IF EXISTS {table}_index"
        tx.execute(template.format(table=table))

    @staticmethod
    def get(tx, repository_id, item_id, item_class):
        table = SQLItem.get_table(repository_id)
        params = dict(item_id=item_id, item_class=item_class)
        template = """
            SELECT item_id, item_class, signature, serial, data 
            FROM {table}
            WHERE item_id = :item_id AND item_class = :item_class
        """
        tx.execute(template.format(table=table), params)
        result = tx.fetchone()
        if result is not None:
            return SQLItem(*result)

    @staticmethod
    def get_all(tx, repository_id):
        table = SQLItem.get_table(repository_id)
        template = """
            SELECT item_id, item_class, signature, serial, data 
            FROM {table}
            ORDER BY item_class ASC, serial ASC
        """
        tx.execute(template.format(table=table))
        return map(lambda x: SQLItem(*x), tx.fetchall())

    @staticmethod
    def get_signatures(tx, repository_id):
        table = SQLItem.get_table(repository_id)
        template = """
            SELECT signature
            FROM {table}
            ORDER BY item_class ASC, serial ASC
        """
        tx.execute(template.format(table=table))
        return map(lambda x: x[0], tx.fetchall())

    @staticmethod
    def get_by_index(tx, repository_id, item_class, key, value):
        table = SQLItem.get_table(repository_id)
        params = dict(item_class=item_class, key=key, value=value)
        template = """
            SELECT DISTINCT i.item_id, i.item_class, i.signature, i.serial, i.data 
            FROM {table} i
            LEFT JOIN {table}_index ii 
                ON (i.item_id = ii.item_id AND i.item_class = ii.item_class)
            WHERE ii.key = :key AND ii.value = :value AND ii.item_class = :item_class
            ORDER BY i.item_id ASC, i.item_class ASC
        """
        tx.execute(template.format(table=table), params)
        return map(lambda x: SQLItem(*x), tx.fetchall())

    @staticmethod
    def get_by_class(tx, repository_id, item_class):
        table = SQLItem.get_table(repository_id)
        params = dict(item_class=item_class)
        template = """
            SELECT item_id, item_class, signature, serial, data 
            FROM {table}
            WHERE item_class = :item_class
            ORDER BY item_id ASC, item_class ASC
        """
        tx.execute(template.format(table=table), params)
        return map(lambda x: SQLItem(*x), tx.fetchall())

    @staticmethod
    def insert(tx, repository_id, item, indexes):
        table = SQLItem.get_table(repository_id)
        params = dict(item_id=item.item_id,
                      item_class=item.item_class,
                      signature=item.signature,
                      serial=item.serial,
                      data=item.data)
        template = """
            INSERT INTO {table} (
            item_id, item_class, signature, serial, data
            ) values (
            :item_id, :item_class, :signature, :serial, :data
            )
        """
        tx.execute(template.format(table=table), params)

        for index in indexes:
            params = dict(item_id=item.item_id,
                          item_class=item.item_class,
                          key=index.key,
                          value=index.value)
            template = """
                INSERT INTO {table}_index (
                item_id, item_class, key, value
                ) values (
                :item_id, :item_class, :key, :value
                )
            """
            tx.execute(template.format(table=table), params)

    @staticmethod
    def delete(tx, repository_id, item_id, item_class):
        table = SQLItem.get_table(repository_id)
        params = dict(item_id=item_id, item_class=item_class)
        template = """
            DELETE FROM {table} WHERE item_id = :item_id AND item_class = :item_class
        """
        tx.execute(template.format(table=table), params)

    @staticmethod
    def get_table(repository_id):
        return 'items_{0}'.format(repository_id.lower())
