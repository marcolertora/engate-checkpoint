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

from twisted.internet import reactor
from twisted.internet.defer import Deferred


class TransientDeferred(Deferred):

    def __init__(self, timeout, canceller=None):
        Deferred.__init__(self, canceller=canceller)
        self.eraser = reactor.callLater(timeout, self.cancel)

    def stop_eraser(self):
        if self.eraser.active():
            self.eraser.cancel()

    def callback(self, result):
        self.stop_eraser()
        Deferred.callback(self, result)

    def errback(self, fail=None):
        self.stop_eraser()
        Deferred.errback(self, fail)

    def cancel(self):
        self.stop_eraser()
        Deferred.cancel(self)


