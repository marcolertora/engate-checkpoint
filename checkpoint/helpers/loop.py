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
from twisted.logger import Logger
from twisted.internet.defer import inlineCallbacks, Deferred


class LoopShouldWait(Exception):
    pass


class LoopInteraction(object):

    log = Logger()

    def __init__(self, initialize, interaction, interval=60, limit_min_threshold=1, limit_max_threshold=1000):
        assert callable(initialize), 'initialize should be callable'
        assert callable(interaction), 'interaction should be callable'

        self.initialize = initialize
        self.interaction = interaction
        self.interval = interval
        self.limit_max_threshold = limit_max_threshold
        self.limit_min_threshold = limit_min_threshold
        self.defer = None
        self.running = True

    def start(self):
        self.running = True
        self.defer = self.initialize()
        assert isinstance(self.defer, Deferred), 'initialize should return a defer'
        self.defer.addCallback(lambda x: self.run_interaction())
        # TODO: could be removed?
        self.defer.addErrback(self.log.failure)

    def stop(self):
        self.running = False
        if self.defer and self.defer.active():
            self.defer.cancel()

    @inlineCallbacks
    def run_interaction(self):
        limit = self.limit_min_threshold
        try:
            while self.running:
                defer = self.interaction(limit)
                assert isinstance(defer, Deferred), 'interaction should return a defer'
                yield defer
                limit = min(limit * 2, self.limit_max_threshold)

            self.log.debug('has been stopped, exit', interval=self.interval)

        except LoopShouldWait:
            self.log.debug('waiting for {interval} seconds..', interval=self.interval)
            reactor.callLater(self.interval, self.start)

    @inlineCallbacks
    def initialize(self):
        raise NotImplementedError

    @inlineCallbacks
    def interaction(self):
        raise NotImplementedError
