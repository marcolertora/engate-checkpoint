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

import voluptuous as vol
from configuration import val
from twisted.internet import reactor
from node import Node
from event import Event


class State(Node):
    """
    state node can be reached from an action node or from a state node through a event node.
    state node can lead to an other state node or an action through a event node.
    when automaton lands on a state node a timer for timeout is started, when it leave the node the timer is stopped
    """

    __slots__ = Node.__slots__ + ['timeout', 'timer']

    CONFIG_SCHEMA = Node.CONFIG_SCHEMA.extend({
        vol.Optional('timeout'): val.timeout,
    })

    def __init__(self, node_id, config):
        config = State.CONFIG_SCHEMA(config)
        super(State, self).__init__(node_id, config)
        self.timeout = config.get('timeout')
        self.timer = None

    def add_edge(self, through, to_node, edge_config=None):
        assert isinstance(through, Event), 'in state starting edge through should be an event'
        super(State, self).add_edge(through, to_node, edge_config)

    def enter(self, parent, edge_config, **kwargs):
        """is there is a previous current state exit from it the set this as current"""
        self.log.debug('entering...')
        if parent.current_state:
            parent.current_state.exit()

        self.start_timer(parent)
        parent.set_current_state(self, **kwargs)

    def exit(self):
        self.log.debug('exiting...')
        self.stop_timer()

    def handle_event(self, parent, label, **kwargs):
        """is called when an event is triggered and automaton is in this state"""
        self.next_node(label, parent, **kwargs)

    def start_timer(self, parent):
        if self.timeout is not None:
            self.timer = reactor.callLater(self.timeout, lambda: parent.timeout_event.trigger())

    def stop_timer(self):
        if self.timer is not None and self.timer.active():
            self.timer.cancel()
