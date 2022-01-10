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

from argparse import Namespace
from collections import namedtuple
from twisted.internet.defer import inlineCallbacks, returnValue, maybeDeferred
from output import OutputDevice
from input import InputDevice
from helpers import async_sleep

EventKey = namedtuple('EventKey', ['unit', 'port', 'value'])


class InputRelay(InputDevice):

    def get_event_key(self, link_config):
        """event are discriminated using unit port and value"""
        assert 'port' in link_config, 'no port configured in link'
        assert 'value' in link_config, 'no value configured in link'
        return EventKey(link_config.get('unit'), link_config['port'], link_config['value'])

    def on_port_changed(self, unit, port, value):
        self.log.info('unit {unit} port {port} is changed to {value}',
                      unit=unit,
                      port=port,
                      value=value)
        self.trigger_events(key=EventKey(unit, port, value))


class OutputRelay(OutputDevice):

    Action = Namespace(SET='set', CHECK='check')

    def set_port(self, unit, port, value):
        raise NotImplementedError

    def get_port(self, unit, port):
        raise NotImplementedError

    def check_port(self, unit, port, value):
        current_value = yield maybeDeferred(self.get_port, unit, port)
        returnValue(current_value == value)

    @inlineCallbacks
    def pulse_port(self, unit, port, value, duration):
        yield self.set_port(unit, port, not value)
        yield self.set_port(unit, port, value)
        yield async_sleep(duration)
        yield self.set_port(unit, port, not value)

    @inlineCallbacks
    def fire(self, link_config, automaton, edge_config, **kwargs):
        assert 'port' in link_config, 'port is required'
        operation = link_config.get('operation', OutputRelay.Action.SET)
        unit = link_config.get('unit')
        port = link_config['port']
        value = link_config.get('value', True)
        duration = link_config.get('duration')
        count = link_config.get('count', 1)

        if operation == OutputRelay.Action.CHECK:
            self.log.info('checking unit {unit} port {port} for value {value}...',
                          unit=unit,
                          port=port,
                          value=value)
            result = yield maybeDeferred(self.check_port, unit, port, value)
            self.log.info('unit {unit} port {port} has been checked, result {result}',
                          unit=unit,
                          port=port,
                          result=result)
            returnValue(result)
            return

        if operation == OutputRelay.Action.SET and duration is None:
            self.log.info('setting unit {unit} port {port} to {value}...',
                          unit=unit,
                          port=port,
                          value=value)
            yield maybeDeferred(self.set_port, unit, port, value)
            self.log.info('unit {unit} port {port} has been set',
                          unit=unit,
                          port=port)
            return

        if operation == OutputRelay.Action.SET and duration is not None:
            assert isinstance(count, int), 'count should be integer'
            self.log.info('setting unit {unit} port {port} to {value} for {secs} secs {count} times...',
                          unit=unit,
                          port=port,
                          value=value,
                          secs=duration,
                          count=count)

            for item in range(count):
                yield maybeDeferred(self.pulse_port, unit, port, value, duration)
                self.log.info('unit {unit} port {port} has been set',
                              unit=unit,
                              port=port)
            return

        raise NotImplementedError('unknown action: {0}'.format(operation))
