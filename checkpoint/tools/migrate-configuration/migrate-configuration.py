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

import os
import sys
import argparse
import psycopg2
from psycopg2.extras import DictCursor
from ruamel.yaml import YAML, scalarstring
from ruamel.yaml.comments import CommentedMap
from automaton import Node
from configuration import Yaml
from helpers import load_module


class LegacyConfig(object):

    @staticmethod
    def row_to_dict(transcode, items):
        return dict(map(transcode, items))

    def __init__(self, tx, folder=None, stdout=None, use_name=False):
        self.tx = tx
        self.stdout = stdout
        self.use_name = use_name
        self.folder = folder
        self.default_name = ''
        self.default_automaton_id = 'DEBUG'
        self.directions = ('IN', 'OUT', 'THROUGH')
        self.sec_levels = dict()
        self.sec_levels_index = dict()
        self.lane_status = dict()
        self.lane_types = dict()
        self.default_automaton_nodes = dict()
        self.transit_status = dict()
        self.devices = dict()
        self.consoles = dict()
        self.devices_index = dict()
        self.sites = dict()
        self.automatons = dict()

    def select(self, table, order=None, where=None):
        query = 'SELECT * FROM {0}'.format(table)
        if where:
            query += ' WHERE ' + where
        if order:
            query += ' ORDER BY ' + order
        self.tx.execute(query)
        return self.tx.fetchall()

    def load_from_databases(self):
        print 'loading transit status...'
        self.transit_status = self.get_transit_status()
        print 'loading security levels...'
        self.sec_levels = self.get_sec_levels()
        self.sec_levels_index = self.get_sec_levels_index()
        print 'loading lane status...'
        self.lane_status = self.get_lane_status()
        print 'loading lane types...'
        self.lane_types = self.get_lane_types()
        print 'loading default automaton nodes...'
        self.default_automaton_nodes = self.get_default_automaton_nodes()
        print 'loading devices...'
        self.devices = self.get_devices()
        self.devices_index = self.get_devices_index()
        print 'loading consoles...'
        self.consoles = self.get_consoles()
        print 'loading sites...'
        self.sites = self.get_sites()
        print 'loading automatons...'
        self.automatons = self.get_automatons()

    def dump_yaml(self, data, filename):
        yaml = YAML()
        yaml.version = (1, 1)
        scalarstring.walk_tree(data)

        if self.stdout:
            yaml.dump(data, sys.stdout)
            return

        assert self.folder, 'invalid folder {0}'.format(self.folder)
        filename = os.path.join(self.folder, filename)
        print 'dumping {0}...'.format(filename)
        yaml.dump(data, open(filename, 'w'))

    def load_yaml(self, filename):
        assert self.folder, 'invalid folder {0}'.format(self.folder)
        yaml = Yaml(root_folder=self.folder)
        return yaml.load_config_from_filename(filename, append_root_folder=False)

    def get_lane_status(self):

        def _transcode(_row):
            item = CommentedMap()
            item['name'] = _row['lanestatus_name']
            return _row['lanestatus_id'], item

        return LegacyConfig.row_to_dict(_transcode, self.select('lanestatus', order='lanestatus_id'))

    def get_transit_status(self):

        def _transcode(_row):
            item = CommentedMap()
            item['name'] = _row['tstatus_description']
            item['color'] = _row['tstatus_color']
            if _row['tstatus_timeout'] > 0:
                item['timeout'] = _row['tstatus_timeout']
            return _row['tstatus_id'], item

        return LegacyConfig.row_to_dict(_transcode, self.select('tstatus', order='tstatus_id'))

    def get_lane_types(self):

        def _transcode(_row):
            item = CommentedMap()
            item['name'] = _row['description']

            # if _row['lanetype_flags']:
            #    item['tags'] = _row['lanetype_flags'].split('|')

            default_config = CommentedMap()
            default_config['automaton'] = self.default_automaton_id
            default_config['check_operator'] = bool(_row['operatorauth'])
            default_config['check_vehicle'] = bool(_row['checkplate'])
            item['default'] = default_config

            overrides = self.get_overrides(_row['lanetype_id'])
            if len(overrides):
                item['overrides'] = overrides

            return _row['lanetype_id'], item

        return LegacyConfig.row_to_dict(_transcode, self.select('lanetypes', order='lanetype_id'))

    def get_devices(self):

        def _cast_attribute(key, value):
            if key in ('units',):
                return map(int, value.split('|'))
            if key in ('listen_port',):
                return int(value)
            if key in ('interval',):
                return float(value)
            if key in ('mirror',):
                return bool(value)
            if key in ('private_key',):
                return str(value)
            raise KeyError('unknown device config: {0}={1}'.format(key, value))

        def _transcode(_row):

            item = CommentedMap()
            if not self.use_name:
                item['name'] = _row['device_name']

            device_factory = _row['device_class']
            try:
                load_module('devices', device_factory)
            except ImportError:
                raise ValueError('invalid device factory {0}'.format(device_factory))

            item['factory'] = device_factory

            if _row['host'] is not None:
                item['host'] = _row['host']

            if _row['port'] is not None:
                item['port'] = _row['port']

            if device_factory == 'TARGET':
                item['url'] = 'http://{0}:{1}/'.format(_row['host'], _row['port'])
                del item['host']
                del item['port']

            if not _row['enabled']:
                item['disabled'] = True

            # append device specific attributes
            for _row_config in self.select('deviceconfig',
                                           order='device_id, param_key',
                                           where='device_id = {0}'.format(_row['device_id'])):
                key, value = _row_config['param_key'], _row_config['param_value']
                if value is not None:
                    item[key] = _cast_attribute(key, _row_config['param_value'])

            return _row['device_name'] if self.use_name else _row['device_id'], item

        return LegacyConfig.row_to_dict(_transcode, self.select('devices', 'device_id'))

    def get_devices_index(self):

        def _transcode(_row):
            return _row['device_id'], _row['device_name']

        return LegacyConfig.row_to_dict(_transcode, self.select('devices', order='device_id'))

    def get_sec_levels(self):

        def _transcode(_row):
            item = CommentedMap()
            item['name'] = self.default_name if self.use_name else _row['description']
            return _row['description'] if self.use_name else _row['securitylevel_id'], item

        return LegacyConfig.row_to_dict(_transcode, self.select('securitylevels', order='securitylevel_id'))

    def get_sec_levels_index(self):

        def _transcode(_row):
            return _row['securitylevel_id'], _row['description']

        return LegacyConfig.row_to_dict(_transcode, self.select('securitylevels', order='securitylevel_id'))

    @staticmethod
    def _cast_automaton_node_attribute(key, value):
        if key in ('remotemethod', 'action', 'port', 'status'):
            return str(value)
        if key in ('timeout',):
            return int(value)
        if key in ('pulse',):
            return float(value)
        if key in ('flag',):
            return bool(value)
        if key in ('checks',):
            return value.split('|')

        raise KeyError('unknown automaton node config: {0}={1}'.format(key, value))

    def get_lane_device_links(self, lane_id):

        def _transcode(_row):
            # links are ordered by priority, priority is replaced by ordered array
            item = CommentedMap()

            device_id = _row['device_id']
            assert device_id in self.devices_index, 'invalid device {0}'.format(device_id)
            item['device'] = self.devices_index[device_id] if self.use_name else device_id

            node_name = _row['node_name']
            assert node_name is not None, 'node cannot be null {0}'.format(node_name)
            assert node_name in self.default_automaton_nodes, 'invalid node {0}'.format(node_name)

            if node_name.startswith('E'):
                item['event'] = node_name
            elif node_name.startswith('A'):
                item['action'] = node_name
            else:
                raise ValueError('unknown node type {0}'.format(node_name))

            if not _row['enabled']:
                item['disabled'] = True

            # add config from removed default automanode action/event
            item.update(self.default_automaton_nodes[node_name])

            # add link specific attributes
            for _row_config in self.select('lanes_devices_config',
                                           order='id, param_key',
                                           where='id = {0}'.format(_row['id'])):
                key, value = _row_config['param_key'], _row_config['param_value']
                if value is not None:
                    item[key] = self._cast_automaton_node_attribute(key, _row_config['param_value'])

            return item

        return map(_transcode, self.select('lanes_devices',
                                           order='device_id, priority ASC',
                                           where='lane_id = {0}'.format(lane_id)))

    def get_lanes(self, gate_id):

        def _transcode(_row):
            item = CommentedMap()
            if not self.use_name:
                item['name'] = _row['lane_name']

            direction = _row['direction_id']
            assert direction in self.directions, 'invalid direction {0}'.format(direction)
            item['direction'] = direction

            lane_type_id = _row['lanetype_id']
            assert lane_type_id in self.lane_types, 'invalid lane type {0}'.format(lane_type_id)
            item['type'] = _row['lanetype_id']

            lane_status_id = _row['lanestatus_id']
            assert lane_status_id in self.lane_status, 'invalid lane status {0}'.format(lane_status_id)
            item['initial_status'] = lane_status_id

            if not _row['enabled']:
                item['disabled'] = True

            item['device_links'] = self.get_lane_device_links(_row['lane_id'])

            return _row['lane_name'] if self.use_name else _row['lane_id'], item

        return LegacyConfig.row_to_dict(_transcode, self.select('lanes',
                                                                order='lane_id',
                                                                where='gate_id = {0}'.format(gate_id)))

    def get_gate_console_links(self, gate_id):
        consoles = list()
        links = self.load_yaml('gate_console_links.yaml')
        for console_id in links.get(gate_id, list()):
            assert console_id in self.consoles, 'invalid console {0}'.format(console_id)
            consoles.append(console_id)

        return consoles

    def get_gates(self, site_id):

        def _transcode(_row):
            item = CommentedMap()

            if not self.use_name:
                item['name'] = _row['gate_name']

            sec_level_id = _row['securitylevel_id']
            assert sec_level_id in self.sec_levels_index, 'invalid security level {0}'.format(sec_level_id)
            item['initial_security_level'] = self.sec_levels_index[sec_level_id] if self.use_name else sec_level_id

            # pass_back_interval = 0 (default) means disabled
            if bool(_row['antipassback']):
                item['pass_back_interval'] = int(_row['antipassbackttl'])

            if _row['location']:
                item['latitude'], item['longitude'] = map(float, _row['location'].split(';', 2))

            if not _row['enabled']:
                item['disabled'] = True

            item['consoles'] = self.get_gate_console_links(_row['gate_name'] if self.use_name else _row['gate_id'])
            item['lanes'] = self.get_lanes(_row['gate_id'])

            return _row['gate_name'] if self.use_name else _row['gate_id'], item

        return LegacyConfig.row_to_dict(_transcode, self.select('gates',
                                                                order='gate_id',
                                                                where='site_id = {0}'.format(site_id)))

    def get_sites(self):

        def _transcode(_row):
            item = CommentedMap()
            if not self.use_name:
                item['name'] = _row['site_name']
            item['gates'] = self.get_gates(_row['site_id'])
            return _row['site_name'] if self.use_name else _row['site_id'], item

        return LegacyConfig.row_to_dict(_transcode, self.select('sites', order='site_id'))

    def get_overrides(self, lane_type_id):

        def _get_config(_row):
            item = CommentedMap()
            item['automaton'] = _row['automa_id']

            if _row['checkplate'] is not None:
                item['check_vehicle'] = bool(_row['checkplate'])

            if _row['checkzone'] is not None:
                item['check_zone'] = bool(_row['checkzone'])

            if _row['checkbiometric'] is not None:
                item['check_biometric'] = bool(_row['checkbiometric'])

            if _row['checkoperator'] is not None:
                item['check_operator'] = bool(_row['checkoperator'])

            if _row['checkprofile'] is not None:
                item['check_zone'] = bool(_row['checkprofile'])

            return item

        def _get_selectors(_row):
            selectors = CommentedMap()

            if _row['lanestatus_id'] is not None:
                selectors['lane_status'] = _row['lanestatus_id']

            sec_level_id = _row['securitylevel_id']
            if _row['securitylevel_id'] is not None:
                selectors['security_level'] = self.sec_levels_index[sec_level_id] if self.use_name else sec_level_id

            if _row['direction_id'] is not None:
                selectors['direction'] = _row['direction_id']

            return selectors

        def _transcode(_row):
            item = CommentedMap()
            item['selectors'] = _get_selectors(_row)
            item['config'] = _get_config(_row)
            return item

        return map(_transcode, self.select('lanetypes_automas',
                                           order='laneautoma_id',
                                           where='lanetype_id = {0!r}'.format(lane_type_id)))

    def get_default_automaton_nodes(self):

        def _transcode(_row):
            item = CommentedMap()
            # append node custom attributes
            for _row_config in self.select('automanodeconfig',
                                           order='automanode_id, param_key',
                                           where='automanode_id = {0!r}'.format(_row['automanode_id'])):
                key, value = _row_config['param_key'], _row_config['param_value']
                if value is not None:
                    item[key] = self._cast_automaton_node_attribute(key, _row_config['param_value'])
            return _row['automanode_id'], item

        return LegacyConfig.row_to_dict(_transcode, self.select('automanodes', order='automanode_id'))

    def get_automatons(self):

        def _transcode(_row):
            item = CommentedMap()
            if _row['automa_name']:
                item['name'] = _row['automa_name']

            if not _row['enabled']:
                item['disabled'] = True

            edges = self.get_automaton_edges(_row['automa_id'])
            if edges:
                item['edges'] = edges

            states = dict()
            for edge in edges:
                for node_id in [edge['from'], edge['to']]:
                    if node_id and node_id.startswith('S'):
                        base_id = Node.full_to_base_id(node_id)
                        if base_id in self.default_automaton_nodes:
                            config = self.default_automaton_nodes[base_id]
                            if len(config):
                                states[base_id] = config

            if len(states):
                item['states'] = states

            return _row['automa_id'], item

        return LegacyConfig.row_to_dict(_transcode, self.select('automas', order='automa_id'))

    @staticmethod
    def fix_node_id(node_id):
        if node_id in ['X@CatchAllBegin', 'X@CatchAllEnd']:
            return node_id.replace('X@', 'S@')

        return node_id

    def get_automaton_edges(self, automa_id):

        def _transcode(_row):
            item = CommentedMap()

            assert _row['entry_start'] is not None, 'invalid edge start node'
            if _row['entry_start']:
                item['from'] = LegacyConfig.fix_node_id(_row['entry_start'])

            assert _row['entry_next'] is not None, 'invalid edge start node'
            item['to'] = LegacyConfig.fix_node_id(_row['entry_next'])

            if _row['entry_edge']:
                item['through'] = _row['entry_edge']

            if not _row['enabled']:
                item['disabled'] = True

            # append automaton edge custom attributes
            where = 'automaedge_id = {0} AND automa_id = {1!r}'.format(_row['automaedge_id'], _row['automa_id'])
            for _row_config in self.select('automaedgeconfig', where=where):
                key, value = _row_config['param_key'], _row_config['param_value']
                if value is not None:
                    item[key] = LegacyConfig._cast_automaton_node_attribute(key, _row_config['param_value'])

            return item

        return map(_transcode, self.select('automaedges',
                                           order='entry_start',
                                           where='automa_id = {0!r}'.format(automa_id)))

    def get_consoles(self):

        def _cast_attribute(key, value):
            if key in ('message',):
                return str(value)
            raise KeyError('unknown console config: {0}={1}'.format(key, value))

        def _transcode(_row):
            item = CommentedMap()
            if not self.use_name:
                item['name'] = _row['console_name']

            console_factory = _row['consoleclass_id']

            try:
                load_module('consoles', console_factory)
            except ImportError:
                raise ValueError('invalid console factory {0}'.format(console_factory))

            item['factory'] = console_factory

            item['host'] = _row['host']
            item['port'] = _row['port']

            if not _row['enabled']:
                item['disabled'] = True

            # append console custom attributes
            for _row_config in self.select('consoleconfig',
                                           order='console_id, param_key',
                                           where='console_id = {0}'.format(_row['console_id'])):
                key, value = _row_config['param_key'], _row_config['param_value']
                if value is not None:
                    item[key] = _cast_attribute(key, _row_config['param_value'])

            return _row['console_name'] if self.use_name else _row['console_id'], item

        return LegacyConfig.row_to_dict(_transcode, self.select('consoles', order='console_id'))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('host',
                        type=str,
                        help='database server host')
    parser.add_argument('--database',
                        type=str,
                        default='igate',
                        metavar='name',
                        help='database name (default: %(default)s)')
    parser.add_argument('--user',
                        type=str,
                        default='igate',
                        help='database user (default: %(default)s)')
    parser.add_argument('--password',
                        type=str,
                        default='igate',
                        help='database password (default: %(default)s)')
    parser.add_argument('--port',
                        type=int,
                        default=5432,
                        help='database server port (default: %(default)d)')
    parser.add_argument('--folder',
                        type=str,
                        metavar='folder',
                        default='.',
                        help='output folder (default: %(default)s)')
    parser.add_argument('--use-name',
                        action='store_true',
                        dest='use_name',
                        help='use name instead of numeric id (default: %(default)s)')
    parser.add_argument('--stdout',
                        action='store_true',
                        help='output to stdout (default: %(default)s)')

    args = parser.parse_args()
    connection = psycopg2.connect(database=args.database, user=args.user, password=args.password, host=args.host)
    cursor = connection.cursor(cursor_factory=DictCursor)
    a = LegacyConfig(cursor, folder=args.folder, stdout=args.stdout, use_name=args.use_name)
    a.load_from_databases()
    a.dump_yaml(a.sec_levels, 'security_levels.yaml')
    a.dump_yaml(a.lane_status, 'lane_status.yaml')
    a.dump_yaml(a.lane_types, 'lane_types.yaml')
    a.dump_yaml(a.consoles, 'consoles.yaml')
    a.dump_yaml(a.devices, 'devices.yaml')
    a.dump_yaml(a.sites, 'sites.yaml')
    a.dump_yaml(a.automatons, 'automatons.yaml')
    a.dump_yaml(a.transit_status, 'transit_status.yaml')
    cursor.close()
    connection.close()
