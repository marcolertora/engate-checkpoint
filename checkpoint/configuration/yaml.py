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

from glob import glob

from _ordereddict import ordereddict
from ruamel.yaml import YAML, os, BaseConstructor


class YamlException(Exception):
    pass


class Yaml(YAML):
    SECRET_FILENAME = 'secrets.yaml'

    @staticmethod
    def _compose_document(self):
        """Remove initialize anchors to empty dict in order to allow yaml merge across included file"""

        self.parser.get_event()
        node = self.compose_node(None, None)
        self.parser.get_event()
        return node

    @staticmethod
    def _yaml_include(constructor, node):
        """Include yaml file, wildcard are allowed"""

        parent_yaml = constructor.loader.__class__(root_folder=constructor.loader.root_folder,
                                                   typ=constructor.loader.typ)
        parent_yaml.composer.anchors = constructor.loader.composer.anchors

        paths = glob(os.path.join(constructor.loader.root_folder, node.value))

        if not len(paths):
            raise YamlException('no files found: {0}'.format(node.value))

        # FIXME: when round-trip it should return CommentedMap
        values = ordereddict()
        yaml_values = map(lambda y: parent_yaml.load_config_from_filename(y, append_root_folder=False), paths)
        for key, value in [x for d in yaml_values if d is not None for x in d.items()]:
            if not constructor.loader.allow_duplicated and key in values:
                raise YamlException('duplicated key found {}'.format(key))
            values[key] = value

        return values

    @staticmethod
    def _yaml_secret(constructor, node):
        """Load secrets from an external yaml file and embed it"""

        parent_yaml = constructor.loader.__class__(root_folder=constructor.loader.root_folder,
                                                   typ=constructor.loader.typ)
        secrets = parent_yaml.load_config_from_filename(constructor.loader.secret_filename)

        if not isinstance(secrets, dict):
            raise YamlException('invalid secrets file: it should be a dictionary')

        if node.value not in secrets:
            raise YamlException('missing key {0} in secrets file'.format(node.value))

        return secrets[node.value]

    @staticmethod
    def _yaml_relative_path(constructor, node):
        """Load relative path"""
        if os.path.isabs(node.value):
            return str(node.value)

        if not constructor.loader.root_folder:
            raise YamlException('cannot use relative path without root_folder')

        return os.path.join(constructor.loader.root_folder, str(node.value))

    def __init__(self, root_folder='.', secret_filename=None, typ=None):
        """Add support for !include and !secret and load_config"""
        super(Yaml, self).__init__(typ=typ, pure=True)
        self.default_flow_style = False
        self.allow_duplicated = True
        self.root_folder = root_folder
        self.secret_filename = secret_filename if secret_filename else Yaml.SECRET_FILENAME
        self.Constructor.add_constructor('!include', Yaml._yaml_include)
        self.Constructor.add_constructor('!secret', Yaml._yaml_secret)
        self.Constructor.add_constructor('!relative_path', Yaml._yaml_relative_path)
        self.Composer.compose_document = Yaml._compose_document

    def load_config_from_filename(self, filename, append_root_folder=True):
        """Read yaml config from path in root_folder"""

        if append_root_folder:
            filename = os.path.join(self.root_folder, filename)

        try:
            stream = open(filename, 'r')
            return self.load(stream)
        except IOError, err:
            raise YamlException(err)


if __name__ == '__main__':
    yaml = Yaml(typ='rt', root_folder='config/')
    data = yaml.load_config_from_filename('checkpoint.yaml')
    print(data)
