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
from pydoc import locate


def traverse(path, data, start='', wildcard='*', optional='?', separator='/'):
    """
    get values by path from structured data, wildcard is used to iterate items
    path: should terminate with separator
    """

    def _traverse(_path, _data, _key):
        return traverse(path, _data, start + _key + separator,
                        wildcard=wildcard,
                        optional=optional,
                        separator=separator)

    if not len(path):
        return [(start, data)]

    assert path.endswith(separator), 'path should ends with {0}'.format(separator)

    key, path = path.split(separator, 1)

    if key == wildcard:
        if isinstance(data, dict):
            return sum(map(lambda (x, y): _traverse(path, y, x), data.items()), [])
        if isinstance(data, list):
            return sum(map(lambda (x, y): _traverse(path, y, str(x)), enumerate(data)), [])

        raise TypeError('wanted list or dict got {0}'.format(type(data)))

    if key.startswith(optional):
        key = key.lstrip(optional)
        if key not in data:
            return []

    return _traverse(path, data[key], key)


def load_module(path, module):
    module_full_name = '{0}.{1}'.format(path, module)
    module = locate(module_full_name)
    if module is None:
        raise ImportError('module not found: {0}'.format(module_full_name))
    return module
