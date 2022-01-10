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


from device import Biometric
from rsi import RSI
from device.protocols import ProtocolSerial


class HGRProto(ProtocolSerial):
    """
        Beep --> HereIsStatus
        SendTemplate --> HereIsTemplate
        SendStatusCRC --> HereIsStatus
        Abort --> HereIsStatus
        EnrollUser --> HereIsStatus
        VerifyOnExternalData --> HereIsStatus
    """
    READY, VERIFYING, ENROLLING = 'READY', 'VERIFYING', 'ENROLLING'

    def __init__(self, polling_interval, left_hand=False):
        ProtocolSerial.__init__(self, polling_interval)
        self.hand = 1 if left_hand else 0
        self.unit = RSI()
        self.current_state = HGRProto.READY
        self.message_factory = RSI.parsePackets

    def connectionMade(self):
        ProtocolSerial.connectionMade(self)
        self.next_message()
        self.watchdog()

    def get_next_polling_message(self):
        return self.unit.SendStatusCRC()

    def enroll(self):
        self.current_state = HGRProto.ENROLLING
        self.add_message(self.unit.EnrollUser(self.hand))

    def abort(self):
        self.current_state = HGRProto.READY
        self.add_message(self.unit.Abort())

    def beep(self):
        self.add_message(self.unit.Beep(7, 2))

    def verify(self, template):
        self.current_state = HGRProto.VERIFYING
        self.add_message(self.unit.VerifyOnExternalData(self.hand, str(template)))

    def handle_messages(self, messages):
        self.set_last_seen()

        for message in messages:
            operation = message['command']
            self.factory.device_log.debug('received {operation}/{state}', operation=operation, state=self.current_state)

            if operation == 'HereIsStatus':

                if self.current_state in (HGRProto.VERIFYING, HGRProto.ENROLLING):

                    if message['status'].FAILED_CMD:
                        self.current_state = HGRProto.READY
                        self.factory.on_failure('unknown error')

                    if message['status'].RSLTS_RDY:
                        self.add_message(self.unit.SendTemplate())

            if operation == 'HereIsTemplate':

                if self.current_state == HGRProto.ENROLLING:
                    self.current_state = HGRProto.READY
                    self.factory.on_enroll_complete(message['template'])
                    self.beep()

                if self.current_state == HGRProto.VERIFYING:
                    self.current_state = HGRProto.READY
                    self.factory.on_verify_complete(self.normalize_score(message['score']), message['template'])
                    self.beep()

            self.next_message()

    def normalize_score(self, origin_score):
        # HGR score is 0-250 where 0 is perfect match
        # sometime score is 2222 it means no match at all
        origin_score = min(origin_score, RSI.SCORE.MAX)
        assert RSI.SCORE.MIN <= origin_score <= RSI.SCORE.MAX, 'score out of range'
        # reverse the score. 250 now is perfect match
        score = RSI.SCORE.MAX - origin_score
        # convert to 0-100 range where 100 is perfect match
        score = (score * Biometric.SCORE.MAX / RSI.SCORE.MAX)
        self.factory.device_log.info('origin {origin} normalized {normalized}', origin=origin_score, normalized=score)
        return score
