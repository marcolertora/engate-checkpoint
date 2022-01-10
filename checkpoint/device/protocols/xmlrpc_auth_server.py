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

from twisted.web import http
from twisted.web.xmlrpc import XMLRPC


class XMLRPCAuth(XMLRPC):
    """A class which works as an XML-RPC server with HTTP basic authentication"""

    factory = None

    def __init__(self, username=None, password=None, **kwargs):
        self.username = username
        self.password = password
        XMLRPC.__init__(self, **kwargs)

    def render_POST(self, request):

        if self.username:
            username = request.getUser()
            password = request.getPassword()

            if not username or not password:
                request.setResponseCode(http.UNAUTHORIZED)
                return 'Authorization required!'

            if username != self.username or password != self.password:
                request.setResponseCode(http.UNAUTHORIZED)
                return 'Authorization Failed!'

        return XMLRPC.render_POST(self, request)
