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

import binascii
from twisted.internet.defer import inlineCallbacks, CancelledError, returnValue
from twisted.web import xmlrpc
from twisted.web.xmlrpc import XMLRPC, Proxy
from device import DeviceException, Biometric
from exceptions import EnrollmentException
from helpers import XMLRPCExceptions


class RpcEnrollment(XMLRPC):

    def __init__(self, log, stations, force_http_client):
        XMLRPC.__init__(self, allowNone=True)
        self.log = log
        self.stations = stations
        self.force_http_client = force_http_client

    @inlineCallbacks
    def xmlrpc_read_badge(self, station_id, timeout):
        """
        :param station_id: station identifier
        :param timeout: number of seconds to wait for a tag read
        :return: string badge code
        :raise: Exception, 8000: no data read, 8001: something wrong
        """
        self.log.debug('read badge {station} {timeout}',
                       station=station_id,
                       timeout=timeout)
        try:
            station = self.get_station(station_id)
            badges = yield station.badge.read_badge(timeout)
            if len(badges) == 0:
                raise CancelledError()
            if not len(badges) == 1:
                raise EnrollmentException('too many badges read')

            returnValue(badges[0].code)

        except CancelledError:
            returnValue(xmlrpc.Fault(8000, 'no data read'))

        except (EnrollmentException, DeviceException) as err:
            returnValue(xmlrpc.Fault(8001, 'something wrong: {0}'.format(err)))

    @inlineCallbacks
    def xmlrpc_acquire_biometric(self, station_id, biometric_type_id, name):
        """
        :param station_id: station identifier
        :param biometric_type_id: biometric type identifier
        :param name: something to show on device display
        :return: base64 encoded biometric template
        :raise: Exception, 8000: no data read, 8001: something wrong
        """
        self.log.debug('acquire biometric {station} {biometric_type} {name}',
                       station=station_id,
                       biometric_type=biometric_type_id,
                       name=name)
        try:
            station = self.get_station(station_id)
            new_template = yield station.biometric.enroll(biometric_type_id, name)
            if not new_template:
                raise CancelledError()
            returnValue(new_template.encode('base64'))

        except CancelledError:
            returnValue(xmlrpc.Fault(8000, 'no data read'))

        except (EnrollmentException, DeviceException) as err:
            returnValue(xmlrpc.Fault(8001, 'something wrong: {0}'.format(err)))

    @inlineCallbacks
    def xmlrpc_verify_biometric(self, station_id, biometric_type_id, template, threshold, name):
        """
        :param station_id: station identifier
        :param biometric_type_id: biometric type identifier
        :param template: base64 encoded biometric template
        :param threshold: threshold above match is evaluated successful (0-100, 100 is perfect match)
        :param name: something to show on device display
        :return: dictionary is_valid: true on successful match, false otherwise score: score
        :raise: Exception, 8000: no data read, 8001: something wrong, 8003: invalid parameters
        """
        self.log.debug('verify biometric {station} {biometric_type} {template} {threshold} {name}',
                       station=station_id,
                       biometric_type=biometric_type_id,
                       template=template,
                       threshold=threshold,
                       name=name)

        try:
            template = template.decode('base64')
        except binascii.Error:
            returnValue(xmlrpc.Fault(8003, 'invalid template'))

        if not isinstance(threshold, int):
            returnValue(xmlrpc.Fault(8003, 'invalid threshold'))
        if not Biometric.SCORE.MIN <= threshold <= Biometric.SCORE.MAX:
            returnValue(xmlrpc.Fault(8003, 'threshold out of range'))

        try:
            station = self.get_station(station_id)
            is_valid, score, new_template = yield station.biometric.verify(biometric_type_id, template, threshold, name)
            self.log.debug('biometric verified: result: {result} score {score}', result=is_valid, score=score)
            returnValue(dict(is_valid=is_valid, score=score))

        except CancelledError:
            returnValue(xmlrpc.Fault(8000, 'no data read'))

        except (EnrollmentException, DeviceException) as err:
            returnValue(xmlrpc.Fault(8001, 'something wrong: {0}'.format(err)))

    def xmlrpc_readBadge(self, lane_id, params):
        self.log.debug('read badge {lane} {params}',
                       lane=lane_id,
                       params=params)
        d = self.read_badge(lane_id, params)
        d.addErrback(self.log.failure)
        return True

    def xmlrpc_acquireBiometric(self, lane_id, params, biometric_type_id, name):
        self.log.debug('acquire biometric {lane} {params} {biometric_type} {name}',
                       lane=lane_id,
                       params=params,
                       biometric_type=biometric_type_id,
                       name=name)
        d = self.acquire_biometric(lane_id, params, biometric_type_id, name)
        d.addErrback(self.log.failure)
        return True

    def xmlrpc_verifyBiometric(self, lane_id, params, biometric_type_id, template, threshold, name):
        self.log.debug('verify biometric {lane} {params} {biometric_type} {template}, {threshold}, {name}',
                       lane=lane_id,
                       params=params,
                       biometric_type=biometric_type_id,
                       template=template,
                       threshold=threshold,
                       name=name)
        d = self.verify_biometric(lane_id, params, biometric_type_id, template, threshold, name)
        d.addErrback(self.log.failure)
        return True

    def xmlrpc_acquirePicture(self, lane_id, params, name):
        raise NotImplementedError

    def get_station(self, station_id):
        if station_id not in self.stations:
            raise EnrollmentException('invalid station_id {0}'.format(station_id))
        return self.stations[station_id]

    def get_station_legacy(self, lane_id):
        for station_id in self.stations:
            if lane_id == self.stations[station_id].legacy_lane_id:
                return self.stations[station_id]
        raise EnrollmentException('invalid lane_id {0}'.format(lane_id))

    @inlineCallbacks
    def read_badge(self, lane_id, params):
        timeout = 10
        self.log.info('reading badge for {timeout} secs...', timeout=timeout)
        try:
            station = self.get_station_legacy(lane_id)
            badges = yield station.badge.read_badge(timeout)
            assert len(badges) > 0, 'need at least one badge'
            yield self.read_badge_response(params, badges[0].code, badges[0].code_type)
        except (EnrollmentException, CancelledError, DeviceException), err:
            self.log.warn('reading badge {err!r}', err=err)
            yield self.cancel_response(params, 'cancelled: {0}'.format(err))

    @inlineCallbacks
    def acquire_biometric(self, lane_id, params, biometric_type_id, name):
        self.log.info('acquiring biometric {biometric_type}...', biometric_type=biometric_type_id)
        try:
            new_template = yield self.get_station_legacy(lane_id).biometric.enroll(biometric_type_id, name)
            yield self.enroll_biometric_response(params, new_template)
        except (EnrollmentException, CancelledError, DeviceException), err:
            self.log.warn('acquiring biometric {err!r}', err=err)
            yield self.cancel_response(params, 'cancelled: {0}'.format(err))

    @inlineCallbacks
    def verify_biometric(self, lane_id, params, biometric_type_id, template, threshold, name):
        template = template.decode('base64')
        self.log.info('verifying biometric {biometric_type}...', biometric_type=biometric_type_id)
        try:
            station = self.get_station_legacy(lane_id)
            is_valid, score, new_template = yield station.biometric.verify(biometric_type_id, template, threshold, name)
            yield self.verify_biometric_response(params, new_template, score)
        except (EnrollmentException, CancelledError, DeviceException), err:
            self.log.warn('verifying biometric {err!r}', err=err)
            yield self.cancel_response(params, 'cancelled: {0}'.format(err))

    @inlineCallbacks
    def read_badge_response(self, params, code, code_type):
        yield self.response(params, 'ClientService.onGateReadBadge', code, code_type)

    @inlineCallbacks
    def enroll_biometric_response(self, params, template):
        template = template.encode('base64')
        yield self.response(params, 'ClientService.onGateAcquireBiometric', template, list())

    @inlineCallbacks
    def verify_biometric_response(self, params, template, score):
        template = template.encode('base64')
        yield self.response(params, 'ClientService.onGateVerifyBiometric', template, score, list())

    @inlineCallbacks
    def cancel_response(self, params, message=None):
        yield self.response(params, 'ClientService.onError', message)

    @inlineCallbacks
    def response(self, params, method_name, *args):
        url = params['remoteUrl'] if not self.force_http_client else self.force_http_client
        self.log.info('sending response {method} to {url}...', method=method_name, url=url)

        try:
            proxy = Proxy(url, allowNone=True, connectTimeout=10)
            proxy.queryFactory.noisy = False
            yield proxy.callRemote(method_name, params['sessionId'], params['tokenId'], *args)
        except XMLRPCExceptions, err:
            self.log.warn('response cannot be delivered: {err}', err=err)
        else:
            self.log.info('response sent!')
