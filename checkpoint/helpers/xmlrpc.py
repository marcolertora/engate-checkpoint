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


import xmlrpclib
import httplib
import types
from pyexpat import ExpatError
from twisted.internet.error import ConnectError, ConnectionClosed


XMLRPCExceptions = xmlrpclib.Fault, ConnectError, ConnectionClosed, ExpatError

xmlrpclib.Unmarshaller.dispatch['ex:nil'] = xmlrpclib.Unmarshaller.end_nil


def patch_xmlrpclib():
    import xmlrpclib
    xmlrpclib.Unmarshaller.dispatch['ex:nil'] = xmlrpclib.Unmarshaller.end_nil


class EnhancedTransport(xmlrpclib.Transport):

    def __init__(self, use_datetime=0, timeout=None, username=None, password=None):
        xmlrpclib.Transport.__init__(self, use_datetime)
        self.timeout = timeout
        self.username = username
        self.password = password

    def make_connection(self, host):
        connection = xmlrpclib.Transport.make_connection(self, host)
        if self.timeout:
            if isinstance(connection, httplib.HTTPConnection):
                connection.timeout = self.timeout
            elif isinstance(connection, httplib.HTTP):
                connection._conn.timeout = self.timeout
            else:
                raise NotImplementedError
        return connection

    def get_host_info(self, host):
        x509 = {}
        extra_headers = None
        if isinstance(host, types.TupleType):
            host, x509 = host
        if self.username and self.password:
            auth = '%s:%s' % (self.username, self.password)
            extra_headers = [('Authorization', 'Basic ' + auth.encode('base64').strip())]
        return host, extra_headers, x509


class EnhancedServerProxy(xmlrpclib.ServerProxy):

    def __init__(self, uri, timeout=None, username=None, password=None, **kw):
        transport = EnhancedTransport(use_datetime=kw.get('use_datetime'),
                                      timeout=timeout,
                                      username=username,
                                      password=password)
        xmlrpclib.ServerProxy.__init__(self, uri, transport=transport, **kw)
