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


class SQLMessage(object):

    def __init__(self, queue_id, message_class, data, num_of_attempts=0):
        self.queue_id = queue_id
        self.message_class = message_class
        self.data = data
        self.num_of_attempts = num_of_attempts

    @staticmethod
    def get_next(tx):
        template = """
            SELECT queue_id, message_class, data, num_of_attempts
            FROM message_queue
            ORDER BY num_of_attempts ASC, queue_id ASC 
            LIMIT 1
        """
        tx.execute(template)
        result = tx.fetchone()
        if result is not None:
            return SQLMessage(*result)

    @staticmethod
    def get_all_by_class(tx, message_class):
        params = dict(message_class=message_class)
        template = """
            SELECT queue_id, message_class, data, num_of_attempts
            FROM message_queue
            WHERE message_class = :message_class
            ORDER BY queue_id DESC
        """
        tx.execute(template, params)
        return map(lambda x: SQLMessage(*x), tx.fetchall())

    @staticmethod
    def count(tx):
        template = """
            SELECT count(*) AS count
            FROM message_queue
        """
        tx.execute(template)
        result = tx.fetchone()
        return result[0] if result is not None else 0

    @staticmethod
    def insert(tx, message):
        params = dict(queue_id=message.queue_id,
                      message_class=message.message_class,
                      data=message.data,
                      num_of_attempts=message.num_of_attempts)

        template = """
            INSERT INTO message_queue (
            queue_id, message_class, data, num_of_attempts
            ) values (
            :queue_id, :message_class, :data, :num_of_attempts
            )
        """
        tx.execute(template, params)

    @staticmethod
    def update_num_of_attempts(tx, queue_id, num_of_attempts):
        params = dict(queue_id=queue_id, num_of_attempts=num_of_attempts)
        template = """
            UPDATE message_queue SET
            num_of_attempts = :num_of_attempts
            WHERE queue_id = :queue_id
        """
        tx.execute(template, params)

    @staticmethod
    def delete(tx, queue_id):
        params = dict(queue_id=queue_id)
        template = """
            DELETE FROM message_queue WHERE queue_id = :queue_id
        """
        tx.execute(template, params)

    @staticmethod
    def create(tx):
        template = """
            CREATE TABLE IF NOT EXISTS message_queue (
                queue_id VARCHAR(64),
                message_class VARCHAR(16), 
                data VARCHAR,
                num_of_attempts INTEGER,
                PRIMARY KEY(queue_id)
            )
        """
        tx.execute(template)

        template = """
            CREATE UNIQUE INDEX IF NOT EXISTS message_queue_idx_1
            ON message_queue (queue_id ASC)
        """
        tx.execute(template)

        template = """
            CREATE UNIQUE INDEX IF NOT EXISTS message_queue_idx_2
            ON message_queue (queue_id ASC, message_class ASC)
        """
        tx.execute(template)

        template = """
            CREATE INDEX IF NOT EXISTS message_queue_idx_3
            ON message_queue (num_of_attempts ASC, queue_id ASC)
        """
        tx.execute(template)
