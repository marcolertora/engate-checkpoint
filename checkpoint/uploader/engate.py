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
import uuid
from argparse import Namespace
import voluptuous as vol
from twisted.internet.defer import inlineCallbacks
from backends import ItemNotFound
from configuration import val
from helpers import JsonServerProxy, JSONRPCException, LoopInteraction, LoopShouldWait, class_name, JSONRPCHTTPException
from base import UploaderBase
from uploader.engate_mapper import map_message
from uploader.exceptions import UploaderDuplicatedException, UploaderVersionException


class UploaderEnGate(UploaderBase):

    __slots__ = UploaderBase.__slots__ + ['endpoints', 'buffer', 'buffer_size', 'loop',
                                          'drop_mismatch_format_version_message']

    CONFIG_SCHEMA = UploaderBase.CONFIG_SCHEMA.extend({
        vol.Required('interval', default=60.0): val.interval,
        vol.Required('drop_mismatch_format_version_message', default=False): bool,
        vol.Required('endpoints'): {
            vol.Any(vol.Extra): vol.Schema({
                vol.Required('base_url'): vol.Url(),
                vol.Required('method'): str,
                vol.Required('username', default=None): vol.Maybe(str),
                vol.Required('password', default=None): vol.Maybe(str),
                vol.Required('http_timeout', default=120): val.timeout,

            })
        }
    })

    HTTP_ERROR_CODE = Namespace(MESSAGE_DUPLICATED=409, MESSAGE_MALFORMED=400)

    def __init__(self, config, checkpoint):
        super(UploaderEnGate, self).__init__(config, checkpoint)
        self.buffer = list()
        self.endpoints = dict()
        self.drop_mismatch_format_version_message = config['drop_mismatch_format_version_message']
        for endpoint_id in config['endpoints']:
            url = config['endpoints'][endpoint_id]['base_url'] + config['endpoints'][endpoint_id]['method']
            self.endpoints[endpoint_id] = JsonServerProxy(url,
                                                          config['endpoints'][endpoint_id]['username'],
                                                          config['endpoints'][endpoint_id]['password'],
                                                          config['endpoints'][endpoint_id]['http_timeout'])

        self.loop = LoopInteraction(initialize=self.backend.initialize,
                                    interaction=self.interaction,
                                    interval=config['interval'])

    def starting(self):
        self.loop.start()

    @property
    def backend(self):
        return self.checkpoint.backend.uploader

    def insert_in_queue(self, message_item):
        """ insert message in queue """
        queue_id = uuid.uuid4().hex.upper()
        self.log.debug('adding {message_item} in queue with {queue_id}', message_item=message_item, queue_id=queue_id)
        message_class = class_name(message_item)
        message_dict = map_message(message_item)
        self.log.debug('{message_item} data {message_dict!r}', message_item=message_item, message_dict=message_dict)
        self.backend.insert_message(queue_id, message_class, message_dict)

    @inlineCallbacks
    def delete_from_queue(self, queue_id):
        """ insert message in queue """
        self.log.debug('removing {queue_id} from queue', queue_id=queue_id)
        yield self.backend.delete_message(queue_id)

    @inlineCallbacks
    def send_message(self, message):
        """ send message to remote """
        try:
            yield self.endpoints[message.message_class].post(message.data)
        except JSONRPCHTTPException as err:
            if err.http_code == UploaderEnGate.HTTP_ERROR_CODE.MESSAGE_DUPLICATED:
                raise UploaderDuplicatedException(*err.args)
            if err.http_code == UploaderEnGate.HTTP_ERROR_CODE.MESSAGE_MALFORMED:
                if self.drop_mismatch_format_version_message:
                    raise UploaderVersionException(*err.args)
            raise

    @inlineCallbacks
    def interaction(self, limit):
        """ send message from queue to endpoint """
        try:
            message = yield self.backend.get_next_message()
            count = yield self.backend.count_message()

        except ItemNotFound as err:
            raise LoopShouldWait(err)

        try:
            self.log.info('sending {queue_id} ({count} in queue)', queue_id=message.queue_id, count=count)

            if message.message_class not in self.endpoints:
                raise JSONRPCException('no {0} endpoint config'.format(message.message_class))

            yield self.send_message(message)
            self.log.info('{queue_id} has been sent.', queue_id=message.queue_id)
            yield self.delete_from_queue(message.queue_id)

        except UploaderDuplicatedException:
            self.log.info('{queue_id} was already there, bounce', queue_id=message.queue_id)
            yield self.delete_from_queue(message.queue_id)

        except UploaderVersionException:
            self.log.info('{queue_id} mismatch format version, bounce', queue_id=message.queue_id)
            yield self.delete_from_queue(message.queue_id)

        except JSONRPCException as err:
            self.log.error('failed to send {queue_id} {num_of_attempts} attempts {err}',
                           queue_id=message.queue_id,
                           num_of_attempts=message.num_of_attempts,
                           err=err)
            yield self.backend.update_message_num_of_attempts(message.queue_id, message.num_of_attempts + 1)

            if message.num_of_attempts >= 1:
                raise LoopShouldWait('more than one failed attempts')
