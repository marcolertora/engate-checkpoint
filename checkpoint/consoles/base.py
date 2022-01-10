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
from gettext import translation
from twisted.logger import Logger
import voluptuous as vol
from helpers import class_repr, class_str
from helpers import get_root_folder
from messages import LaneMessageFactory
import os


class Console(object):

    __slots__ = ['console_id', 'default_message', 'translation', 'disabled']

    CONFIG_SCHEMA = vol.Schema({
        vol.Required('factory'): object,
        vol.Required('languages', default=[]): [str],
        vol.Required('default_message', default=''): str,
        vol.Required('disabled', default=False): bool,
    })

    log = Logger()
    lane_factory = LaneMessageFactory

    def __init__(self, console_id, config):
        assert isinstance(config, dict), 'invalid config'
        self.console_id = console_id
        self.default_message = config['default_message']
        self.translation = translation('checkpoint',
                                       os.path.join(get_root_folder(), 'locales'),
                                       languages=config['languages'],
                                       fallback=True)
        self.disabled = config['disabled']

    def lane_message_factory(self, lane):
        assert issubclass(self.lane_factory, LaneMessageFactory), 'should inherit LaneMessageFactory'
        return self.lane_factory(self, lane)

    def __repr__(self):
        return class_repr(self, self.console_id)

    def __str__(self):
        return class_str(self, self.console_id)

    def start(self):
        if self.disabled:
            self.log.warn('is disabled, skip start')
            return

        self.log.info('starting...')
        self.starting()

    def starting(self):
        raise NotImplementedError

    def set_default_message(self, default_message):
        """set the console default message, this is called by gate"""
        if self.default_message != default_message:
            self.log.info('change default message from {old} to {new}', old=self.default_message, new=default_message)
            self.default_message = default_message

