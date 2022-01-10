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
from helpers import class_repr, class_str


class Owner(object):

    ANONYMOUS_LABEL = 'Reserved'

    def __init__(self, name, photo_id=None, company=None, tags=None, disabled=False):
        self.owner_id = uuid.uuid4().hex.upper()
        self._name = name
        self.photo_id = photo_id
        self._company = company
        self.tags = tags
        self.disabled = disabled
        self.permissions = list()
        self.biometrics = dict()

    def __repr__(self):
        return class_repr(self, self.name)

    def __str__(self):
        return class_str(self, self.name)

    def add_biometrics(self, biometrics):
        for biometric in biometrics:
            self.biometrics[biometric.biometric_type] = biometric

    def get_biometric(self, biometric_type):
        if biometric_type in self.biometrics:
            return self.biometrics[biometric_type]

    @property
    def is_anonymous(self):
        return False

    @property
    def name(self):
        return self._name if not self.is_anonymous else Owner.ANONYMOUS_LABEL

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def company(self):
        if not self.is_anonymous:
            return self._company

    @company.setter
    def company(self, company):
        self._company = company

    @property
    def credentials(self):
        for permission in self.permissions:
            for credential in permission.credentials:
                yield credential

    def get_credential(self, uid_code):
        for credential in self.credentials:
            if credential.code == uid_code:
                return credential


class OwnerPerson(Owner):

    def __init__(self,
                 name,
                 birth_date,
                 birth_country,
                 anonymous=None,
                 photo_id=None,
                 company=None,
                 tags=None,
                 disabled=False):

        super(OwnerPerson, self).__init__(name, photo_id=photo_id, company=company, tags=tags, disabled=disabled)
        self._birth_date = birth_date
        self._birth_country = birth_country
        self.anonymous = anonymous

    @property
    def is_anonymous(self):
        return self.anonymous is True

    @property
    def birth_date(self):
        return self._birth_date if not self.is_anonymous else None

    @birth_date.setter
    def birth_date(self, birth_date):
        self._birth_date = birth_date

    @property
    def birth_country(self):
        return self._birth_country if not self.is_anonymous else Owner.ANONYMOUS_LABEL

    @birth_country.setter
    def birth_country(self, birth_country):
        self._birth_country = birth_country


class OwnerVehicle(Owner):

    def __init__(self, name, plate, photo_id=None, company=None, tags=None, disabled=False):
        super(OwnerVehicle, self).__init__(name, photo_id=photo_id, company=company, tags=tags, disabled=disabled)
        self._plate = plate

    @property
    def plate(self):
        return self._plate if not self.is_anonymous else Owner.ANONYMOUS_LABEL

    @plate.setter
    def plate(self, plate):
        self._plate = plate


class OwnerUnknown(Owner):

    def __init__(self):
        super(OwnerUnknown, self).__init__('Unknown')
