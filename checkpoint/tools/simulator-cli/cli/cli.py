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

from __future__ import unicode_literals

from twisted.internet import threads, reactor
from prompt_toolkit.shortcuts import CompleteStyle
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.patch_stdout import patch_stdout
from prompt_toolkit.application import get_app
from prompt_toolkit.contrib.regular_languages.compiler import compile

from device.devices.simulator import SimulatorException
from helpers import inline_dict
from completion import MyNestedCompleter
from common import LoggerCLI
from common import InvalidCommand


class CallableNestedCompleter(MyNestedCompleter):

    def __init__(self, options, follow=None, ignore_case=True):
        super(CallableNestedCompleter, self).__init__(options, ignore_case)
        self.follow = follow if follow is not None else dict()

    def get_completions(self, document, complete_event):
        assert callable(self.options), 'option should be a callable'
        options = {x: MyNestedCompleter.from_nested_dict(self.follow) for x in self.options()}
        completer = MyNestedCompleter(options, ignore_case=self.ignore_case)
        for c in completer.get_completions(document, complete_event):
            yield c


class SimulatorCLI(object):

    log = LoggerCLI()

    @staticmethod
    def shutdown():
        app = get_app()
        if app.is_running:
            app.exit(style='class:exiting', exception=KeyboardInterrupt)

    def __init__(self, factory):
        self.factory = factory
        self.history_filename = '.history'
        self.asking = True

    @property
    def completer(self):

        def get_devices():
            return map(lambda x: x.device_id, self.factory.devices)

        struct = {
            'list': {
                'devices': None,
                'clients': None,
            },
            'connect': CallableNestedCompleter(get_devices),
            'disconnect': CallableNestedCompleter(get_devices, {'sss': None, 'sdssd': None}),
            'trigger': {
                'event': CallableNestedCompleter(get_devices, {'sss': None, 'sdssd': None}),
            },
            'quit': None,
        }
        return MyNestedCompleter.from_nested_dict(struct)

    @property
    def grammar(self):
        command = r'(?P<command>[a-z]+)'
        action = r'(?P<action>[a-z]+)'
        argument = r'(?P<argument>[0-9A-z\-_]+)'
        parameters = r'(?P<parameters>[0-9A-z\-_\'=\s]+)'
        expression = r'''
            (\s*{command}\s+{argument}\s*) |
            (\s*{command}\s+{action}\s+{argument}\s+{parameters}\s*)
        '''
        return compile(expression.format(command=command,
                                         action=action,
                                         argument=argument,
                                         parameters=parameters))

    def deferred_run(self):
        defer = threads.deferToThread(self.run)
        defer.addErrback(self.log.failure)
        reactor.addSystemEventTrigger('before', 'shutdown', SimulatorCLI.shutdown)
        return defer

    @staticmethod
    def parse_parameters(text):
        params = dict()
        for param_text in text.split():
            try:
                key, value = param_text.split('=')
            except ValueError:
                raise InvalidCommand('cannot parse parameters')
            params[key.strip()] = value.strip()
        return params

    def run(self):
        grammar = self.grammar
        session = PromptSession(history=FileHistory(self.history_filename))

        while self.asking:
            try:
                with patch_stdout():
                    result = session.prompt('>: ',
                                            completer=self.completer,
                                            auto_suggest=AutoSuggestFromHistory(),
                                            complete_style=CompleteStyle.READLINE_LIKE,
                                            )

                match_grammar = grammar.match(result)

                if not match_grammar:
                    raise InvalidCommand('invalid command')

                match_vars = match_grammar.variables()
                command = match_vars.get('command')

                if command == 'list':
                    target = match_vars.get('argument')
                    if target == 'devices':
                        for index, device in enumerate(self.factory.devices):
                            print '{0}. {1} {2!r}'.format(index, device.device_id, device.device_config)

                    elif target == 'clients':
                        for index, client in enumerate(self.factory.clients):
                            print '{0}. {1}'.format(index, client.peer)

                    else:
                        raise InvalidCommand('unknown target for list')

                elif command == 'connect':
                    device_id = match_vars.get('argument')
                    assert device_id is not None, 'invalid device'
                    device = self.factory.get_client(device_id)
                    print 'connect {0}'.format(device.peer)

                elif command == 'disconnect':
                    device_id = match_vars.get('argument')
                    assert device_id is not None, 'invalid device'
                    device = self.factory.get_client(device_id)
                    print 'disconnect {0}'.format(device.peer)

                elif command == 'trigger':
                    device_id = match_vars.get('argument')
                    assert device_id is not None, 'invalid device'
                    action = match_vars.get('action')
                    assert action is not None, 'invalid action'
                    if action == 'event':
                        event_params = SimulatorCLI.parse_parameters(match_vars.get('parameters'))
                        print 'trigger event on device {0} {1} '.format(device_id, inline_dict(event_params))
                        self.factory.trigger_event(device_id, event_params)

                elif result == 'quit':
                    raise KeyboardInterrupt

                else:
                    raise InvalidCommand('unknown action')

            except (SimulatorException, InvalidCommand), e:
                print e

            except KeyboardInterrupt:
                break
