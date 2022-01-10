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

import configuration.validation.automaton
from through import Through, ThroughType
from node import Node, NodeType
from helpers import class_repr, class_str


class Edge(object):

    __slots__ = ['from_node', 'to_node', 'through', 'automaton']

    CONFIG_SCHEMA = vol.Schema({
        vol.Required('from'): configuration.validation.automaton.AutomatonNode(NodeType.S, NodeType.A, allow_serial=True),
        vol.Required('to'): configuration.validation.automaton.AutomatonNode(NodeType.S, NodeType.A, allow_serial=True),
        vol.Optional('through'): configuration.validation.automaton.AutomatonThrough(ThroughType.E, ThroughType.L),
        # TODO: add edge validation
        # if from=state through must be event and to must be action
        # if from=action through must be choice and to could be action or state,
        # if through is not provided default choice is used. event is always specified
    }).extend(Node.CONFIG_SCHEMA_EXTRA)

    def __init__(self, config, automaton):
        self.automaton = automaton
        self.from_node = self.automaton.load_node(config['from'])
        self.to_node = self.automaton.load_node(config['to'])
        self.through = Through.load_through(config.get('through'), automaton)
        # attach edge to the from node
        self.from_node.add_edge(self.through, self.to_node, config)

    def __repr__(self):
        return class_repr(self, from_node=self.from_node, to_node=self.to_node, through=self.through)

    def __str__(self):
        return class_str(self)

    @property
    def nodes(self):
        return [self.from_node, self.to_node]
