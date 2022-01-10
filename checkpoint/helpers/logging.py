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

import sys
from twisted.logger import FileLogObserver, formatEventAsClassicLogText, formatTime, timeFormatRFC3339, \
    FilteringLogObserver, LogLevel, LogLevelFilterPredicate, Logger, globalLogBeginner


log_level_names = list(map(lambda x: x.name, LogLevel.iterconstants()))


def format_w_prefix(event):
    if event.get('log_source'):
        event['log_format'] = u'{0} {1}'.format(event.get('log_source'), event.get('log_format'))

    return formatEventAsClassicLogText(
        event, formatTime=lambda e: formatTime(e, timeFormatRFC3339)
    )


def initialize_logging(level_name):
    log = Logger()
    level = LogLevel.levelWithName(level_name)
    observer = FileLogObserver(sys.stdout, format_w_prefix)
    predicates = [LogLevelFilterPredicate(defaultLogLevel=level)]
    log.info('Start logging with level {level_name}...', level_name=level_name)
    globalLogBeginner.beginLoggingTo([FilteringLogObserver(observer=observer, predicates=predicates)])
