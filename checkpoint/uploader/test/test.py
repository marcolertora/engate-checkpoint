#!/usr/bin/env python
# -*- mode:python; tab-width: 4; coding: utf-8 -*-
#
# igate-designer
#
# Copyright (C) 2020 Marco Lertora <marco.lertora@gmail.com>
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
#
from cerberus import Validator, schema_registry, rules_set_registry
from ruamel.yaml import YAML

document = {'uid': 'prova',
            'granted': None,
            'status': {'id': 'st01', 'label': 'pippo'},
            'direction': 'THROUGH',
            }

schema_filename = 'Transit.yaml'
definition_filename = 'Definition.yaml'
definitions_rule = 'DefinitionRule.yaml'

with open(definition_filename, 'r') as definition_stream:
    with open(definitions_rule, 'r') as definitions_rule_stream:
        definitions = YAML().load(definition_stream)
        definitions_rule = YAML().load(definitions_rule_stream)
        # schema_registry.add('id_and_label', definitions['id_and_label']['schema'])
        # schema_registry.extend(definitions)
        rules_set_registry.extend(definitions_rule)
        # print(schema_registry.all())
        print(rules_set_registry.all())

with open(schema_filename, 'r') as schema_stream:
    schema = YAML().load(schema_stream)
    print(schema)
    cerberus = Validator(schema)

    if not cerberus.validate(dict(root=document)):
        raise Exception(cerberus.errors)

print document