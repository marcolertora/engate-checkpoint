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
from collections import namedtuple

from twisted.logger import Logger
from argparse import Namespace
import voluptuous as vol
from commons import Directions
from helpers import class_repr, class_str

NodeType = Namespace(S='S', A='A')

NodeEdge = namedtuple('NodeEdge', ['to_node', 'config'])


class Node(object):

    __slots__ = ['node_type', 'node_name', 'node_serial', 'edges']

    ID_SEPARATOR = '@'

    # TODO: should be replaced by specific node name and device validation
    CONFIG_SCHEMA_EXTRA = {
        vol.Optional('port'): vol.Any(int, str),  # IO
        vol.Optional('operation'): str,  # IO [set|check]
        vol.Optional('duration'): float,  # IO
        vol.Optional('count'): int,  # IO
        vol.Optional('value'): bool,  # IO
        vol.Optional('status'): str,  # setTransitStatus, setLaneStatus, checkLaneStatus
        vol.Optional('direction'): vol.In(Directions),  # setTransitDirection
        vol.Optional('key'): str,  # biometric, legacy
        vol.Optional('unit'): int,  # FKLIGHT, MONTRAF
        vol.Optional('message'): str,  # edge_config  DISPLAY
        vol.Optional('color'): str,  # edge_config  DISPLAY
        # vol.Optional('duration'): float,  # edge_config DISPLAY
    }
    CONFIG_SCHEMA = vol.Schema({}).extend(CONFIG_SCHEMA_EXTRA)

    log = Logger()

    @staticmethod
    def load_node(node_id, config):
        from state import State
        from action import Action
        node_type, node_name, node_serial = Node.parse_id(node_id)

        if node_type == NodeType.S:
            return State(node_id, config)

        if node_type == NodeType.A:
            return Action(node_id, config)

        raise ValueError('unknown automaton node {0}'.format(node_id))

    @staticmethod
    def dump_id(*args):
        """dump node_id node_type@node_name[@node_serial]"""
        return Node.ID_SEPARATOR.join(args)

    @staticmethod
    def parse_id(node_id):
        """
        parse the node_id node_type@node_name[@node_serial]
        return tuple of node_type, node_name, node_serial
        """
        values = node_id.split(Node.ID_SEPARATOR)
        assert 2 <= len(values) <= 3, 'invalid automaton node: {0}'.format(node_id)
        node_type, node_name = values[:2]
        node_serial = values[2] if len(values) == 3 else None

        return node_type, node_name, node_serial

    @staticmethod
    def full_to_base_id(node_id):
        node_type, node_name, node_serial = Node.parse_id(node_id)
        return Node.dump_id(node_type, node_name)

    def __init__(self, node_id, config):
        self.node_type, self.node_name, self.node_serial = Node.parse_id(node_id)
        self.edges = dict()

    def __repr__(self):
        return class_repr(self, self.full_id)

    def __str__(self):
        return class_str(self, self.full_id)

    @property
    def base_id(self):
        """base_node_id node_type@node_name"""
        return Node.dump_id(self.node_type, self.node_name)

    @property
    def full_id(self):
        """full_node_id node_type@node_name[@node_serial]"""
        if self.node_serial is not None:
            return Node.dump_id(self.base_id, self.node_serial)

        return self.base_id

    def add_edge(self, through, to_node, config=None):

        if through.label in self.edges:
            raise ValueError('edge already defined'.format(self, through.label, to_node))

        self.edges[through.label] = NodeEdge(to_node, config if config else dict())

    def enter(self, parent, edge_config, **kwargs):
        """activate the node, is called when automaton land on this node"""
        raise NotImplementedError

    def exit(self):
        """deactivate the node, is called when automaton move to another node"""
        raise NotImplementedError

    def next_node(self, label, parent, **kwargs):
        self.log.info('following edge through {label}...', label=label)
        assert label in self.edges, 'missing edge through {0}'.format(label)
        assert isinstance(self.edges[label].to_node, Node), 'node is not an automaton node'
        self.edges[label].to_node.enter(parent, self.edges[label].config, **kwargs)
