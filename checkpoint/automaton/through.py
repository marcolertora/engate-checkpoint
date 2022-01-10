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
from helpers import class_repr, class_str

ThroughType = Namespace(L='L', E='E')


class Through(object):

    LABEL_SEPARATOR = '@'

    __slots__ = ['through_type', 'through_name', 'parent']

    log = Logger()

    @staticmethod
    def load_through(through_id, automaton):
        from choice import DefaultChoice, Choice
        from event import Event

        if not through_id:
            return DefaultChoice()

        through_type, through_name = Through.parse_id(through_id)

        if through_type == ThroughType.E:
            return Event(through_id, automaton)

        if through_type == ThroughType.L:
            return Choice(through_id)

        raise ValueError('unknown automaton through {0}'.format(through_id))

    @staticmethod
    def dump_id(*args):
        """dump id through_type@through_name"""
        return Through.LABEL_SEPARATOR.join(args)

    @staticmethod
    def parse_id(label):
        """
        parse the id through_type@through_name
        return tuple of through_type, through_name
        """
        values = label.split(Through.LABEL_SEPARATOR)
        assert len(values) == 2, 'invalid through: {0}'.format(label)
        through_type, through_name = values
        return through_type, through_name

    def __init__(self, through_id):
        self.through_type, self.through_name = Through.parse_id(through_id)

    @property
    def label(self):
        """ generate label through_type@through_name """
        return Through.dump_id(self.through_type, self.through_name)

    def __repr__(self):
        return class_repr(self, self.through_name)

    def __str__(self):
        return class_str(self, self.through_name)
