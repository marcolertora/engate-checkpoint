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
from argparse import Namespace
from collections import deque, namedtuple
from copy import deepcopy
import voluptuous as vol

import configuration.validation.automaton
from node import Node, NodeType
from helpers import class_repr, class_str
from edge import Edge
from event import Event
from action import Action
from state import State


QueuedEvent = namedtuple('QueuedEvent', ['label', 'kwargs'])


class Automaton(object):

    __slots__ = ['automaton_id', 'name', 'disabled', 'edges', 'current_state', 'reload_event', 'process_event',
                 'events_queue', 'reload_needed', 'automaton_parent', 'nodes', 'nodes_config', 'previous_catch_all',
                 'timeout_event']

    SystemNode = Namespace(
        START='S@Start',
        CATCH_ALL_BEGIN='S@CatchAllBegin',
        CATCH_ALL_END='S@CatchAllEnd',
    )

    SystemThrough = Namespace(
        RELOAD='E@reloadEvent',
        INITIALIZE='E@Initialize',
        TIMEOUT='E@Timeout',
    )
    CONFIG_SCHEMA = vol.Schema({
        vol.Optional('name'): str,
        vol.Required('edges', default=[]): [Edge.CONFIG_SCHEMA],
        vol.Required('states', default={}): {
            configuration.validation.automaton.AutomatonNode(NodeType.S): State.CONFIG_SCHEMA},
        vol.Required('actions', default={}): {
            configuration.validation.automaton.AutomatonNode(NodeType.A): Action.CONFIG_SCHEMA},
    })

    log = Logger()

    @staticmethod
    def clone(automaton, parent):
        automaton = deepcopy(automaton)
        automaton.parent = parent
        return automaton

    def __init__(self, automaton_id, config):
        self.automaton_parent = None
        self.automaton_id = automaton_id
        self.name = config.get('name', self.automaton_id)
        self.nodes = dict()
        self.nodes_config = dict(config['states'].items() + config['actions'].items())
        self.edges = map(lambda x: Edge(x, self), config['edges'])
        self.current_state = None
        self.process_event = True
        self.events_queue = deque()
        self.previous_catch_all = None

        # create reload event and add an internal edge
        self.reload_needed = False
        self.reload_event = Event(Automaton.SystemThrough.RELOAD, self)
        self.timeout_event = Event(Automaton.SystemThrough.TIMEOUT, self)
        self.initial_state.add_edge(self.reload_event, self.initial_state)

    @property
    def parent(self):
        assert self.automaton_parent is not None, 'set_parent never invoked'
        return self.automaton_parent

    @parent.setter
    def parent(self, parent):
        self.automaton_parent = parent

    def __repr__(self):
        return class_repr(self, self.automaton_id)

    def __str__(self):
        return class_str(self, self.automaton_id)

    def copy(self, parent):
        automaton = deepcopy(self)
        automaton.parent = parent
        return automaton

    def load_node(self, node_id):
        """return a node from nodes, if not exists load a new one and add to list"""
        if node_id not in self.nodes:
            node_base_id = Node.full_to_base_id(node_id)
            node_config = self.nodes_config.get(node_base_id, dict())
            self.nodes[node_id] = Node.load_node(node_id, node_config)
        return self.nodes[node_id]

    @property
    def actions(self):
        """return a dictionary of the actions used in automaton. they came from nodes"""
        return {node.full_id: node for node in self.nodes.values()
                if isinstance(node, Action)}

    @property
    def states(self):
        """return a dictionary of the states used in automaton. they came from nodes"""
        return {node.full_id: node for node in self.nodes.values()
                if isinstance(node, State)}

    @property
    def events(self):
        """return a dictionary of the event used in automaton. they came from edges"""
        return {edge.through.label: edge.through for edge in self.edges
                if edge.through and isinstance(edge.through, Event)}

    @property
    def initial_state(self):
        node_id = Automaton.SystemNode.START
        assert node_id in self.states, 'missing initial node in {0}'.format(self.automaton_id)
        return self.nodes[node_id]

    @property
    def initialize_event(self):
        return self.events.get(Automaton.SystemThrough.INITIALIZE)

    @property
    def catch_all_begin(self):
        return self.states.get(Automaton.SystemNode.CATCH_ALL_BEGIN)

    @property
    def catch_all_end(self):
        return self.states.get(Automaton.SystemNode.CATCH_ALL_END)

    def handle_event(self, label, **kwargs):
        if not self.parent.ready:
            self.log.info('{event} not processed because not ready', event=label)
            return

        if not self.process_event:
            self.log.info('{event} queued', event=label)
            self.events_queue.append(QueuedEvent(label, kwargs))
            return

        self.process_event = False
        self.log.info('processing {event}...', event=label)

        if label not in self.current_state.edges:
            self.log.info('no edge for {event} in state {state}', event=label, state=self.current_state)

            # try to follow a catch all chain
            if self.catch_all_begin is not None and label in self.catch_all_begin.edges:
                self.log.info('found catch all chain with edge for {event}, following...', event=label)
                self.previous_catch_all = self.current_state
                self.catch_all_begin.handle_event(self, label, **kwargs)
                return

            # unlock queue while processing
            self.process_event = True
            return

        self.current_state.handle_event(self, label, **kwargs)

    def schedule_reload(self):
        """set the reload flag and trigger reload event"""
        self.reload_needed = True
        self.reload_event.trigger()

    def set_current_state(self, state, **kwargs):
        """
        set the given state as current and process event queue, if the given state is initial_state:
          * reload the parent if the flag is set
          * trigger initialize event
        """
        if self.catch_all_end is not None and self.catch_all_end == state:
            assert self.previous_catch_all is not None, 'missing previous catch all node'
            self.log.info('end of catch all chain redirect to previous {node}', node=self.previous_catch_all)
            state = self.previous_catch_all

        if self.current_state is None:
            self.log.info('switching to {to_node}...', to_node=state)
        else:
            self.log.info('switching from {from_node} to {to_node}...', from_node=self.current_state, to_node=state)

        self.current_state = state

        if self.current_state == self.initial_state and self.reload_needed:
            self.current_state.exit()
            self.parent.reload()
            self.reload_needed = False
            return

        # FIXME: if initialize_event raise Exception loop is created
        # when trigger initialize set initialized in kwargs to avoid loop
        if self.current_state == self.initial_state and 'initialized' not in kwargs:
            self.log.info('starting...')
            self.parent.on_automaton_start()
            if self.initialize_event is not None:
                self.initialize_event.trigger(initialized=True)

        self.process_event = True

        # when land on a state flush event in queue
        while self.events_queue:
            if not self.process_event:
                break

            queued_event = self.events_queue.popleft()
            self.log.info('processing {event} from queue...', event=queued_event.label)
            self.handle_event(queued_event.label, **queued_event.kwargs)

    def restart(self):
        self.stop()
        self.start()

    def start(self):
        self.log.info('starting...')
        assert self.current_state is None, 'automaton is not ready to start'
        edge_config = dict()
        self.initial_state.enter(self, edge_config)

    def stop(self):
        self.log.info('stopping....')
        self.events_queue.clear()
        self.parent.on_automaton_reset()
        if self.current_state:
            self.current_state.exit()
            self.current_state = None
