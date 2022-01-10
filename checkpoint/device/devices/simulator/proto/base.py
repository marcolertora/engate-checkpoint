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

import json
from argparse import Namespace
from ..exception import SimulatorException


class SimulatorProtocolMixin(object):
    REQUEST = Namespace(EXECUTE_ACTION='execute_action', TRIGGER_EVENT='trigger_event', ANNOUNCE='announce')
    RESPONSE = Namespace(ACK='ack')

    factory = None

    def onMessage(self, payload, is_binary):
        """called on message receive. they can be request or response"""

        assert not is_binary, 'invalid binary message'
        packet = json.loads(payload.decode('utf8'))

        keys = packet.keys()
        assert len(keys) == 1, 'single key dict is required'
        assert keys[0] in ('request', 'response'), 'invalid packet {0}'.format(packet)

        if 'request' in packet:
            self.dispatch_request(packet['request'])

        if 'response' in packet:
            self.dispatch_response(packet['response'])

    def dispatch_request(self, request):
        """dispatch rpc request to factory methods named on_{method}"""

        assert 'method' in request, 'method must be in request'
        method = request['method']
        args = request.get('args', list())
        assert isinstance(args, list), 'args must be a list'

        try:
            method_name = 'on_{0}'.format(method)
            if not hasattr(self.factory, method_name):
                raise SimulatorException('unavailable method {0}'.format(method))

            getattr(self.factory, method_name)(self, *args)
            self.send_ack()

        except SimulatorException as e:
            self.sendClose(1000, u'exception raised: {0}'.format(e))

    def dispatch_response(self, response):
        if response != SimulatorProtocolMixin.RESPONSE.ACK:
            raise SimulatorException('unknown response {0}'.format(response))

    def send_request(self, method, *args):
        data = dict(request=dict(method=method, args=args))
        self.sendMessage(json.dumps(data).encode('utf8'))

    def send_response(self, response):
        data = dict(response=response)
        self.sendMessage(json.dumps(data).encode('utf8'))

    def send_ack(self):
        self.send_response(SimulatorProtocolMixin.RESPONSE.ACK)
