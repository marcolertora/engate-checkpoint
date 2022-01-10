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

from twisted.internet.defer import inlineCallbacks
from twisted.web.resource import Resource

from backends import ItemNotFound
from file import FileResource


class UserPhotoResource(FileResource):

    def __init__(self, checkpoint, repository_id, photo_id):
        FileResource.__init__(self)
        self.checkpoint = checkpoint
        self.photo_id = photo_id
        self.repository_id = repository_id

    @inlineCallbacks
    def deferred_render_GET(self, request):
        try:
            photo = yield self.checkpoint.downloader.get_photo(self.repository_id, self.photo_id)
            self.render_image(request, photo.stream, photo.content_type)
        except ItemNotFound:
            self.render_not_found(request, 'not found: {0}'.format(self.photo_id))


class UserPhoto(Resource):

    def __init__(self, checkpoint, repository_id):
        Resource.__init__(self)
        self.checkpoint = checkpoint
        self.repository_id = repository_id

    def getChild(self, path, request):
        return UserPhotoResource(self.checkpoint, self.repository_id, path)


class getUserImage(FileResource):
    # TODO: remove after grace period

    def __init__(self, checkpoint, repository_id):
        FileResource.__init__(self)
        self.checkpoint = checkpoint
        self.repository_id = repository_id


    @inlineCallbacks
    def deferred_render_GET(self, request):
        try:
            people_id = request.args.get('people_id')
            if not people_id:
                raise ItemNotFound('missing people_id in request')
            photo_id = people_id[0]
            photo = yield self.checkpoint.downloader.get_photo(self.repository_id, photo_id)
            self.render_image(request, photo.stream, photo.content_type)
        except ItemNotFound:
            self.render_not_found(request, 'not found: {0}'.format(photo_id))
