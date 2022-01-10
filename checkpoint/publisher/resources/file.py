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

from datetime import timedelta, datetime
from twisted.internet.defer import maybeDeferred, inlineCallbacks
from twisted.web import http
from twisted.web.resource import Resource
from twisted.web.server import NOT_DONE_YET
from helpers import class_str


class FileResource(Resource):
    isLeaf = True

    def __init__(self):
        Resource.__init__(self)
        self.expire_interval = timedelta(days=1)

    @property
    def header_expires(self):
        expire_date = datetime.now() + self.expire_interval
        return expire_date.strftime('%a, %d %b %Y %T GMT')

    @property
    def header_cache_control(self):
        return 'max-age=%d, public' % self.expire_interval.total_seconds()

    def render_bad_request(self, request, http_code, message):
        request.setResponseCode(http_code)
        request.write('{0}: {1}'.format(class_str(self), message))
        request.finish()

    def render_not_found(self, request, message):
        self.render_bad_request(request, http.NOT_FOUND, message)

    def render_image(self, request, stream, content_type):
        request.setHeader('Content-Type', content_type)
        request.setHeader('Content-Length', str(len(stream)))
        request.setHeader('Cache-Control', self.header_cache_control)
        request.setHeader('Expires', self.header_expires)
        request.write(stream)
        request.finish()

    def render_GET(self, request):
        maybeDeferred(self.deferred_render_GET, request)
        return NOT_DONE_YET

    @inlineCallbacks
    def deferred_render_GET(self, request):
        raise NotImplementedError
