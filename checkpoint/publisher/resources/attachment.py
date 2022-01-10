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

from twisted.web.resource import Resource

from backends import ItemNotFound
from file import FileResource


class AttachmentResource(FileResource):

    def __init__(self, checkpoint, attachment_id):
        FileResource.__init__(self)
        self.checkpoint = checkpoint
        self.attachment_id = attachment_id

    def deferred_render_GET(self, request):
        try:
            attachment = self.checkpoint.get_attachment(self.attachment_id)
            self.render_image(request, attachment.stream, attachment.content_type)
        except ItemNotFound:
            self.render_not_found(request, 'not found: {0}'.format(self.attachment_id))


class Attachments(Resource):

    def __init__(self, checkpoint):
        Resource.__init__(self)
        self.checkpoint = checkpoint

    def getChild(self, path, request):
        return AttachmentResource(self.checkpoint, path)
