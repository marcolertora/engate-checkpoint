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

from twisted.logger import Logger
from copy import deepcopy
from datetime import date
import voluptuous as vol
from backends import ItemNotFound
from commons import AuthCode, AuthStatusId, AuthStatus
from commons.owners import PermissionTags
from commons.transits import TransitMember
from twisted.internet.defer import inlineCallbacks, returnValue
from base import AuthenticatorBase
from gettext import gettext as _


class Authenticator(AuthenticatorBase):

    log = Logger()

    CONFIG_SCHEMA = AuthenticatorBase.CONFIG_SCHEMA.extend({
        vol.Required('repository', default='MOBILE'): str,
    })

    __slots__ = AuthenticatorBase.__slots__ + ['repository_id']

    def __init__(self, config):
        super(Authenticator, self).__init__(config)
        self.repository_id = config['repository']

    @inlineCallbacks
    def get_transit_member(self, identifier):
        member = TransitMember()

        self.log.info('checking identifier {identifier}...', identifier=identifier)
        try:
            credential = yield self.lane.checkpoint.downloader.get_credential(self.repository_id, identifier.code)
        except ItemNotFound:
            self.log.info('no owner found for {identifier}...', identifier=identifier)
            returnValue(member)
        else:
            member.credential = deepcopy(credential)
            member.permission = member.credential.permission
            member.owner = member.credential.permission.owner
            auth = self.validate_credential(credential)
            self.log.info('{identifier} validation response: {auth}...', identifier=identifier, auth=auth)
            member.set_auth(auth)
            self.log.info('{identifier} lead to {member}...', identifier=identifier, member=member)

        returnValue(member)

    def validate_credential(self, credential):
        if credential.valid_from and date.today().toordinal() < credential.valid_from.toordinal():
            return AuthStatus(AuthStatusId.REJECTED, AuthCode.INVALID_DATE, _('credential not yet valid'))

        if credential.valid_to and date.today().toordinal() > credential.valid_to.toordinal():
            return AuthStatus(AuthStatusId.REJECTED, AuthCode.INVALID_DATE, _('credential is expired'))

        if not credential.permission.valid_from or not credential.permission.valid_to:
            return AuthStatus(AuthStatusId.REJECTED, AuthCode.INVALID_DATE, _('invalid permission date'))

        if date.today().toordinal() < credential.permission.valid_from.toordinal():
            return AuthStatus(AuthStatusId.REJECTED, AuthCode.INVALID_DATE, _('permission not yet valid'))

        if date.today().toordinal() > credential.permission.valid_to.toordinal():
            return AuthStatus(AuthStatusId.REJECTED, AuthCode.INVALID_DATE, _('permission is expired'))

        if credential.permission.disabled:
            return AuthStatus(AuthStatusId.REJECTED, AuthCode.INVALID_STATUS, _('permission is disabled'))

        if credential.permission.owner.company and credential.permission.owner.company.disabled:
            return AuthStatus(AuthStatusId.REJECTED, AuthCode.INVALID_COMPANY, _('company is disabled'))

        if self.lane.lane_type_config['check_vehicle']:
            if not credential.permission.has_tag(PermissionTags.vehicle_bypass):
                if not credential.permission.check_vehicle(self.lane.transit.vehicles):
                    return AuthStatus(AuthStatusId.REJECTED,
                                      AuthCode.INVALID_VEHICLE,
                                      _('invalid vehicle'))

        if self.lane.lane_type_config['check_pass_back']:
            if not credential.permission.has_tag(PermissionTags.pass_back_bypass):
                if not credential.permission.check_pass_back(self.lane.direction, self.lane.pass_back_interval):
                    return AuthStatus(AuthStatusId.REJECTED,
                                      AuthCode.INVALID_PASS_BACK,
                                      _('pass back detected'))

        if not self.lane.disable_check_zone:
            if not credential.permission.has_tag(PermissionTags.zone_bypass):
                self.log.info('checking zone...')
                if not credential.permission.check_zone(self.lane.gate.gate_id, self.lane.direction):
                    return AuthStatus(AuthStatusId.REJECTED,
                                      AuthCode.INVALID_LANE,
                                      _('not allowed in this lane'))

        if self.lane.lane_type_config['check_pin']:
            if not credential.permission.has_tag(PermissionTags.pin_bypass):
                return AuthStatus(AuthStatusId.PIN_REQUIRED,
                                  AuthCode.PIN_REQUIRED,
                                  _('valid but pin check is required'))

        if self.lane.lane_type_config['check_biometric']:
            if not credential.permission.has_tag(PermissionTags.biometric_bypass):
                return AuthStatus(AuthStatusId.BIOMETRIC_REQUIRED,
                                  AuthCode.BIOMETRIC_REQUIRED,
                                  _('valid but biometric check is required'))

        if self.lane.lane_type_config['check_operator']:
            if not credential.permission.has_tag(PermissionTags.operator_bypass):
                return AuthStatus(AuthStatusId.OPERATOR_REQUIRED,
                                  AuthCode.OPERATOR_REQUIRED,
                                  _('valid but operator check is required'))

        return AuthStatus(AuthStatusId.ALLOWED, AuthCode.ALLOWED, _('valid'))

    def validate_transit(self):
        self.log.info('validating transit {transit}...', transit=self.lane.transit)
        members = self.lane.transit.members.values()
        escorts = map(lambda x: x.permission.is_escort, members)
        allowed = map(lambda x: x.is_auth, members)
        rejected = map(lambda x: not x.is_auth, members)

        if not len(members):
            self.log.info('reject, no members found')
            return AuthStatusId.REJECTED

        if any(escorts):
            self.log.info('allow, escort member found')
            return AuthStatusId.ALLOWED

        if not any(rejected) and any(allowed):
            self.log.info('allow, no members rejected and at least one allowed')
            return AuthStatusId.ALLOWED

        self.log.info('reject, at least one rejected and no escort members')
        return AuthStatusId.REJECTED

    def validate_pin(self, identifier):
        self.log.info('validating pin {identifier}...', identifier=identifier)
        assert self.lane.transit.current_member.credential, 'invalid current member credential'

        if self.lane.transit.current_member.credential.pin_code == identifier.code:
            return AuthStatusId.ALLOWED

        return AuthStatusId.REJECTED
