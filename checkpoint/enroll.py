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

import argparse
from twisted.logger import Logger
from twisted.internet import reactor
from helpers import logging
from configuration import Yaml
from enrollment import Enrollment

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--config-file',
                        dest='config_file',
                        type=str,
                        default='enrollment.yaml',
                        metavar='filename',
                        help='main config file (default: %(default)s)')
    parser.add_argument('--config-folder',
                        dest='config_folder',
                        type=str,
                        default='config/',
                        metavar='folder',
                        help='config folder (default: %(default)s)')
    parser.add_argument('--log-level',
                        dest='log_level',
                        type=str,
                        default='info',
                        choices=logging.log_level_names,
                        metavar='level',
                        help='logging level (default: %(default)s)')
    parser.add_argument('--enrollment-id',
                        dest='enrollment_id',
                        type=str,
                        default='enrollment01',
                        metavar='id',
                        help='load enrollment id (default: %(default)s)')
    parser.add_argument('--force-simulator',
                        action='store_true',
                        dest='force_simulator',
                        help='force device to use simulator (default: %(default)s)')

    args = parser.parse_args()
    logging.initialize_logging(args.log_level)

    log = Logger()
    log.info('loading and validating yaml configuration from {folder}...', folder=args.config_folder)
    yaml_config = Yaml(args.config_folder).load_config_from_filename(args.config_file)
    config = Enrollment.CONFIG_SCHEMA(yaml_config)

    enrollment = Enrollment(args.enrollment_id, config, args.force_simulator)
    enrollment.start()

    reactor.run()
