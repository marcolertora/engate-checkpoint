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

from twisted.internet.defer import maybeDeferred, DeferredList
from tasks import Tasks
from choice import Choice, DefaultChoice
from node import Node


class Action(Node):
    """
    action node can be reached from an another action node or from a state node through a event node.
    action node can lead to an other action node or to a state node
    a single action node could execute more than one task
    """

    __slots__ = Node.__slots__ + ['attached_tasks', 'user_tasks', 'default_label']

    def __init__(self, node_id, config):
        config = Action.CONFIG_SCHEMA(config)
        super(Action, self).__init__(node_id, config)
        self.attached_tasks = list()
        self.user_tasks = self.get_user_tasks()
        self.default_label = DefaultChoice.LABEL

    def get_user_tasks(self):
        """if the node name match a function name in Actions append to user tasks"""
        tasks = list()
        if self.node_name in Tasks.registered:
            self.log.debug('attaching registered task {task}...', task=self.node_name)
            tasks.append(Tasks.registered[self.node_name])
        return tasks

    @property
    def tasks(self):
        return self.user_tasks + self.attached_tasks

    def add_task(self, action):
        self.attached_tasks.append(action)

    def add_edge(self, through, to_node, edge_config=None):
        assert isinstance(through, Choice), 'in action starting edge through should be an choice {0}'.format(through)
        super(Action, self).add_edge(through, to_node, edge_config)

    @property
    def is_straight_edge(self):
        """xxx has no choices, only the on edge straight to next node xxx"""
        return self.edges.keys() == [DefaultChoice.LABEL]

    def handle_success_and_results(self, success_and_results):
        """
        log failure from task and return two different list results and failures
        """
        results = list()
        failures = list()
        for task_index, (success, value) in enumerate(success_and_results):
            if not success:
                self.log.failure('executing task {task}...', task=task_index + 1, failure=value)
                failures.append(value)
            else:
                results.append(value)

        return results, failures

    def handle_results(self, success_and_results, parent, **kwargs):
        """
        select and lead to next node. selection could be done with value returned from task only with
        single task action otherwise default_label is used. if the single task return none, default_label is used.
        """
        results, failures = self.handle_success_and_results(success_and_results)

        if len(failures):
            self.log.warn('something wrong in tasks executions, restart automaton')
            parent.restart()
            return

        self.log.info('handle results {results}', results=results)
        assert len(results) <= 1 or self.is_straight_edge, 'multiple result and multiple edges are not supported'

        label = self.default_label

        if len(results) == 1 and results[0] is not None:
            label = Choice.result_to_label(results[0])

            # if label not in edge try the default
            if label not in self.edges:
                self.log.warn('no edge through {label}, use default', label=label)
                label = self.default_label

        self.log.info('following label {label}...', label=label)
        self.next_node(label, parent, **kwargs)

    def enter(self, parent, edge_config, **kwargs):
        """
        activate the node, is called when automaton land on this node
        execute all tasks appended to the node
        """
        self.log.debug('entering...')
        self.log.info('executing {count} tasks...', count=len(self.tasks))
        tasks_are_callable = all(map(lambda x: callable(x), self.tasks))
        assert tasks_are_callable, 'not all task are callable in {0}'.format(self.full_id)
        defer_tasks = map(lambda x: maybeDeferred(x, parent, edge_config, **kwargs), self.tasks)
        defer = DeferredList(defer_tasks, consumeErrors=True)
        defer.addCallback(lambda x: self.handle_results(x, parent, **kwargs))
        # FIXME: should wait for defer

    def exit(self):
        self.log.debug('exiting...')
