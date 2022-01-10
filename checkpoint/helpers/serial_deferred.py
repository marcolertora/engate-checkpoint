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

from transient_deferred import TransientDeferred
from twisted.internet.defer import Deferred


class SerialDeferred(object):

    def __init__(self):
        self.defer = None

    def new_deferred(self, timeout=None):
        self.cancel()
        self.defer = TransientDeferred(timeout) if timeout else Deferred()
        return self.defer

    def callback(self, result):
        if self.defer:
            self.defer.callback(result)
            self.defer = None

    def errback(self, fail=None):
        if self.defer:
            self.defer.errback(fail)
            self.defer = None

    def cancel(self):
        if self.defer:
            self.defer.cancel()
            self.defer = None
