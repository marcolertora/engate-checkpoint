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
from twisted.logger import Logger
import voluptuous as vol
from configuration import val
from twisted.web.resource import Resource
from twisted.web.server import Site
from twisted.internet import reactor
from helpers import class_str, class_repr
from resources.user_photo import getUserImage
from resources import UserPhoto, Attachments


class Publisher(object):
    CONFIG_SCHEMA = vol.Schema({
        vol.Required('listen_port'): val.ipv4_port,
        vol.Required('repository', default='MOBILE'): str,
        vol.Required('disabled', default=False): bool,
    })

    __slots__ = ['listen_port', 'checkpoint', 'repository_id', 'disabled']

    log = Logger()

    def __init__(self, config, checkpoint):
        assert config is not None, 'invalid config'
        self.listen_port = config['listen_port']
        self.repository_id = config['repository']
        self.disabled = config['disabled']
        self.checkpoint = checkpoint

    def __repr__(self):
        return class_repr(self)

    def __str__(self):
        return class_str(self)

    @property
    def root_resource(self):
        root = Resource()
        # noinspection PyTypeChecker
        # TODO: remove after grace period
        root.putChild('getUserImage', getUserImage(self.checkpoint, self.repository_id))
        # noinspection PyTypeChecker
        root.putChild('UserPhoto', UserPhoto(self.checkpoint, self.repository_id))
        # noinspection PyTypeChecker
        root.putChild('Attachments', Attachments(self.checkpoint))
        return root

    def start(self):
        if self.disabled:
            self.log.warn('is disabled, skip start')
            return

        self.log.info('starting on {port}...', port=self.listen_port)
        reactor.listenTCP(self.listen_port, Site(self.root_resource))

