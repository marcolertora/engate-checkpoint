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

from address import AddressType


class Company(object):

    def __init__(self, name, company_type, vat=None, disabled=False):
        self.name = name
        self.company_type = company_type
        self.vat = vat
        self.disabled = disabled
        self.addresses = dict()

    @property
    def default_address(self):
        return self.addresses.get(AddressType.DEFAULT)

    def add_address(self, address, address_type=AddressType.DEFAULT):
        self.addresses[address_type] = address
