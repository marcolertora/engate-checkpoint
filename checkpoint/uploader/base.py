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

from helpers import class_str, class_repr


class UploaderBase(object):

    __slots__ = ['checkpoint', 'disabled']

    log = Logger()

    CONFIG_SCHEMA = vol.Schema({
        vol.Required('disabled', default=False): bool,
    })

    def __init__(self, config, checkpoint):
        assert config is not None, 'invalid config'
        self.disabled = config['disabled']
        self.checkpoint = checkpoint

    def __repr__(self):
        return class_repr(self)

    def __str__(self):
        return class_str(self)

    def insert_in_queue(self, message_item):
        """add a message in the queue"""
        raise NotImplementedError

    def delete_from_queue(self, tx, queue_id):
        """delete a message from the queue"""
        raise NotImplementedError

    def start(self):
        """start the uploader loop"""
        if self.disabled:
            self.log.warn('is disabled, skip start')
            return

        self.log.info('starting...')
        self.starting()

    def starting(self):
        raise NotImplementedError
