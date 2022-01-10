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

from argparse import Namespace
from input import InputDevice
from datetime import datetime
from commons import Command
import voluptuous as vol

BiometricType = Namespace(LEFT_HAND='LEFT_HAND',
                          RIGHT_HAND='RIGHT_HAND')


class Biometric(InputDevice):

    # score range is 0-100 and 100 is perfect match
    SCORE = Namespace(MIN=0, MAX=100)

    EVENT_KEY = Namespace(AUTH='AUTH', NO_AUTH='NO_AUTH', FAILURE='FAILURE')

    CONFIG_SCHEMA = InputDevice.CONFIG_SCHEMA.extend({
            vol.Required('update_min', default=80): vol.All(int,  vol.Range(min=0, max=100)),
            vol.Required('update_max', default=100): vol.All(int,  vol.Range(min=0, max=100)),
    })

    def __init__(self, device_id, config, checkpoint, biometric_type):
        super(Biometric, self).__init__(device_id, config, checkpoint)
        self.biometric_type = biometric_type
        self.update_min = config['update_min']
        self.update_max = config['update_max']

    def fire(self, link_config, automaton, edge_config, **kwargs):
        biometric = automaton.parent.transit.current_member.owner.get_biometric(self.biometric_type)
        if not biometric:
            self.log.warn('no biometric for {biometric_type}', biometric_type=self.biometric_type)
            self.on_verify_no_auth(automaton.parent.transit)
            return

        if biometric.bypass:
            self.log.warn('biometric bypass for {biometric_type}', biometric_type=self.biometric_type)
            self.on_verify_auth(automaton.parent.transit)
            return

        template = biometric.get_template(self.device_id)
        if not template:
            self.log.warn('no biometric template for {biometric_type}', biometric_type=self.biometric_type)
            self.on_verify_no_auth(automaton.parent.transit)
            return

        self.verify(automaton.parent.transit, biometric, template)

    def get_event_key(self, link_config):
        assert 'key' in link_config, 'no key configured in link'
        return link_config['key']

    def on_verify_complete(self, score, template, transit, biometric):
        assert Biometric.SCORE.MIN <= score <= Biometric.SCORE.MAX, 'out of biometric score range'

        if biometric.biometric_id and self.update_min <= score <= self.update_max:
            self.log.info('template should be updated for this device')
            command = Command(Command.ACTION.UPDATE_BIOMETRIC,
                              dict(biometric_id=biometric.biometric_id,
                                   device_id=self.device_id,
                                   template=template,
                                   enrollment_timestamp=datetime.now())
                              )
            self.checkpoint.uploader.insert_in_queue(command)

        self.log.info('verify score {score} threshold {threshold}', score=score, threshold=biometric.threshold)
        if self.is_valid_score(score, biometric.threshold):
            self.on_verify_auth(transit)
        else:
            self.on_verify_no_auth(transit)

    @staticmethod
    def is_valid_score(score, threshold):
        return score >= threshold

    def on_failure(self, failure, transit):
        self.log.critical(failure)
        self.trigger_events(key=Biometric.EVENT_KEY.FAILURE, transit=transit)

    def on_verify_auth(self, transit):
        self.trigger_events(key=Biometric.EVENT_KEY.AUTH, transit=transit)

    def on_verify_no_auth(self, transit):
        self.trigger_events(key=Biometric.EVENT_KEY.NO_AUTH, transit=transit)

    def verify(self, transit, biometric, template):
        raise NotImplementedError
