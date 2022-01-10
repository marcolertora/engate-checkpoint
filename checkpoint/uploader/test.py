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

from twisted.internet import reactor
from checkpoint import Checkpoint
from configuration import Yaml
from uploader import Uploader
from commons import Command, LaneLog, DeviceLog

if __name__ == '__main__':
    checkpoint_id = 'checkpoint01'
    yaml_config = Yaml(root_folder='../config').load_config_from_filename('checkpoint.yaml')
    config = Checkpoint.CONFIG_SCHEMA(yaml_config)

    checkpoint = Checkpoint(checkpoint_id, config)
    uploader = Uploader(config['uploader'], checkpoint)
    uploader.start()

    def print_messages(messages):
        for message in messages:
            print 'message: {0}'.format(message)


    a = Command(Command.ACTION.UPDATE_BIOMETRIC, dict(param_a=1, param_b=2))
    uploader.insert_in_queue(a)
    a = LaneLog(12, LaneLog.LEVEL.INFO, LaneLog.CODE.START, 'lane id: 12')
    uploader.insert_in_queue(a)
    a = DeviceLog(12, DeviceLog.LEVEL.INFO, DeviceLog.CODE.NETWORK_LOST, 'device id: 12')
    uploader.insert_in_queue(a)

    reactor.run()
