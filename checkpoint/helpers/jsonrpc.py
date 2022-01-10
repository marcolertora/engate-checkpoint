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
import datetime
import json

import treq
from twisted.internet.defer import inlineCallbacks, returnValue
from twisted.internet.error import ConnectError, DNSLookupError, ConnectingCancelledError
from twisted.web import client, error
from twisted.web._newclient import ResponseFailed, RequestTransmissionFailed

client._HTTP11ClientFactory.noisy = False


class JSONRPCException(Exception):
    pass


class JSONRPCHTTPException(JSONRPCException):

    def __init__(self, message, http_code):
        super(JSONRPCHTTPException, self).__init__(message)
        self.message = message
        self.http_code = http_code

    def __str__(self):
        return '{0}: {1}'.format(self.message, self.http_code)


class JsonServerProxy(object):

    __slots__ = ['base_url', 'username', 'password', 'http_timeout', 'user_agent']

    def __init__(self, base_url, username=None, password=None, http_timeout=None):
        self.base_url = base_url
        self.username = username
        self.password = password
        self.http_timeout = http_timeout
        self.user_agent = 'EnGate Checkpoint'

    @inlineCallbacks
    def request(self, method, path=None, data=None):
        headers = {'Agent': self.user_agent, 'Content-Type': 'application/json'}
        http_auth = self.username, self.password
        url = (self.base_url + path) if path else self.base_url

        def json_converter(o):
            if isinstance(o, datetime.datetime):
                return o.__str__()

        json_data = json.dumps(data, default=json_converter)

        try:
            response = yield treq.request(method,
                                          url,
                                          headers=headers,
                                          timeout=self.http_timeout,
                                          auth=http_auth,
                                          data=json_data)

        except (error.Error,
                ConnectError,
                DNSLookupError,
                ConnectingCancelledError,
                ResponseFailed,
                RequestTransmissionFailed) as err:
            raise JSONRPCException('server return unknown error')

        if response.code in [200, 201]:
            data = yield treq.json_content(response)
            returnValue(data)
            return

        if response.code in [404]:
            raise JSONRPCHTTPException('no item found', http_code=response.code)

        if response.code in [400]:
            message = yield treq.json_content(response)
            raise JSONRPCHTTPException('bad request: {message} - {data}'.format(message=message, data=json_data),
                                       http_code=response.code)

        raise JSONRPCHTTPException('invalid http code', http_code=response.code)

    def get(self, path=None):
        return self.request('GET', path)

    def post(self, data, path=None):
        return self.request('POST', path, data=data)
