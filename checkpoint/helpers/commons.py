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
import json
import sys
import os
from pydoc import locate
from time import time
from traceback import format_exc

import jsonschema
from ruamel.yaml import YAML
from twisted.internet import reactor
from twisted.internet.task import deferLater


def async_sleep(seconds):
    return deferLater(reactor, seconds, lambda: None)


def dict_affinity(keys, item_a, item_b, safe_mode=True):
    """
    compare two given dictionaries using keys order as weight for the key match
    it return affinity score. safe_mode avoid exception for missing key
    """
    score = 0
    keys = list(reversed(keys))
    for index, key in enumerate(keys):
        if safe_mode and not (key in item_a and key in item_b):
            continue
        if None in (item_a[key], item_b[key]):
            continue
        if item_a[key] != item_b[key]:
            return
        score += pow(index + 1, len(keys))
    return score


def class_name(cls):
    """return class name"""
    import inspect
    return cls.__name__ if inspect.isclass(cls) else cls.__class__.__name__


def class_repr(cls, *keys, **kwargs):
    """return class representation"""
    keys = ' '.join(map(str, keys))
    params = inline_dict(kwargs)

    if len(keys) and len(params):
        keys += ' '

    return '<{0}: {1}{2}>'.format(class_name(cls), keys, params)


def class_str(cls, *keys):
    """return str representation"""
    params = u'[{0}]'.format(u' '.join(map(unicode, keys)))
    data = class_name(cls) + params if len(keys) else class_name(cls)
    return data.encode('ascii', 'replace')


def inline_dict(value):
    """return inline representation for dictionary"""
    separator = ', '
    assert isinstance(value, dict), 'value must be a dictionary'
    return separator.join(map(lambda (x, y): '{0}={1}'.format(x, y), value.items()))


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


def get_root_folder():
    return os.path.dirname(sys.argv[0])


def dump_exception_w_payload(payload):
    # FIXME: load from config
    folder = 'dumps/'

    if not os.path.isdir(folder):
        os.mkdir(folder)

    filename = os.path.join(folder, 'packet-{0:.0f}.dump'.format(time() * 100))
    data = dict(payload=payload.encode('hex'), exception=format_exc())

    with open(filename, 'w') as stream:
        YAML().dump(data, stream)


def validate_w_schema(instance, filename):
    schema = json.load(open(filename, 'r'))
    return jsonschema.validate(instance=instance, schema=schema)
