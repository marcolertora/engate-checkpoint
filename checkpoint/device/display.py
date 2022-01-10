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


from configuration import val
import voluptuous as vol
from twisted.internet.defer import inlineCallbacks
from helpers import async_sleep
from output import OutputDevice


class Display(OutputDevice):

    CONFIG_SCHEMA = OutputDevice.CONFIG_SCHEMA.extend({
        vol.Required('duration', default=2.0): val.timeout,
        vol.Required('color', default='000000'): [int],
        vol.Required('encoding', default='latin-1'): str,
    })

    MESSAGE_SEPARATOR = '|'

    def __init__(self, device_id, config, checkpoint):
        super(Display, self).__init__(device_id, config, checkpoint)
        self.default_duration = config['duration']
        self.default_color = config['color']
        self.encoding = config['encoding']

    def clear_display(self):
        raise NotImplementedError

    def write_message(self, message, color):
        raise NotImplementedError

    @inlineCallbacks
    def display_message(self, message, duration, color):
        self.log.info('display message {message:.10}', message=message)
        yield self.write_message(message, color)
        yield async_sleep(duration)

    @inlineCallbacks
    def fire(self, link_config, automaton, edge_config, **kwargs):
        assert 'message' in edge_config, 'action is required'
        message = edge_config.get('message').encode(self.encoding)
        color = edge_config.get('color', self.default_color)
        duration = edge_config.get('duration', self.default_duration)
        self.log.info('fire message {color} {duration} {message:.10}', color=color, duration=duration, message=message)

        yield self.clear_display()
        for page_message in message.split(Display.MESSAGE_SEPARATOR):
            page_message = page_message.format(automaton.parent.transit)
            yield self.display_message(self.compose_message(page_message), duration, color)

    def compose_message(self, message):
        return message
