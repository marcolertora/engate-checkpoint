#!/usr/bin/env python
"""
This is an example of "prompt_toolkit.contrib.regular_languages" which
implements a little calculator.

Type for instance::

    > add 4 4
    > sub 4 4
    > sin 3.14

This example shows how you can define the grammar of a regular language and how
to use variables in this grammar with completers and tokens attached.
"""
from __future__ import unicode_literals
import math

from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.contrib.regular_languages.compiler import compile
from prompt_toolkit.contrib.regular_languages.completion import (
    GrammarCompleter,
)
from prompt_toolkit.contrib.regular_languages.lexer import GrammarLexer
from prompt_toolkit.lexers import SimpleLexer
from prompt_toolkit.shortcuts import CompleteStyle
from prompt_toolkit.styles import Style

devices = map(lambda x: 'ABC{0}'.format(x), range(10))

events = ['AAA', 'BBB']
actionsA = ['list']
argsA = ['devices', 'clients']

actionsB = ['connect', 'disconnect']
argsB = devices

actionsC = ['trigger']
argsC = ['event']
sub_actionsC = ['event']
sub_action_argC = events


def create_grammar():
    """
    list [devices|clients]
    disconnect [device_id|*]
    trigger [device_id|*] [event] [label]
    """
    return compile(r"""
        (\s*(?P<actionA>[a-z]+)\s+(?P<argA>[0-9A-z]+)\s*) |
        (\s*(?P<actionB>[a-z]+)\s+(?P<argB>[0-9A-z]+)\s*) |
        (\s*(?P<actionC>[a-z]+)\s+(?P<argC>[0-9A-z]+)\s+(?P<sub_actionC>[a-z]+)\s+(?P<sub_action_argC>[0-9A-z]+)\s*) |
    """)


class WordCompleterSuffix(WordCompleter):
    suffix = ' '

    def get_completions(self, document, complete_event):
        for item in super(WordCompleterSuffix, self).get_completions(document, complete_event):
            item.text += self.suffix
            yield item


example_style = Style.from_dict({
    'action': '#3333dd bold',
    'device': '#ff0000 bold',
    'argument': '#00FF00 bold',
    'trailing-input': 'bg:#662222 #ffffff',
})

if __name__ == '__main__':
    g = create_grammar()

    lexer = GrammarLexer(g, lexers={
        'actionA': SimpleLexer('class:action'),
        'actionB': SimpleLexer('class:action'),
        'actionC': SimpleLexer('class:action'),
        'sub_actionC': SimpleLexer('class:action'),
        'argA': SimpleLexer('class:argument'),
        'argB': SimpleLexer('class:argument'),
        'argC': SimpleLexer('class:argument'),
        'sub_action_argC': SimpleLexer('class:argument'),

    })

    completer = GrammarCompleter(g, {
        'actionA': WordCompleterSuffix(actionsA),
        'actionB': WordCompleterSuffix(actionsB),
        'actionC': WordCompleterSuffix(actionsC),
        'sub_actionC': WordCompleterSuffix(sub_actionsC),
        'argA': WordCompleterSuffix(argsA),
        'argB': WordCompleterSuffix(devices),
        'argC': WordCompleterSuffix(devices),
        'sub_action_argC': WordCompleterSuffix(events),
    })

    try:
        # REPL loop.
        while True:
            # Read input and parse the result.
            text = prompt('Calculate: ', lexer=lexer, completer=completer,
                          style=example_style, complete_style=CompleteStyle.READLINE_LIKE, )
            m = g.match(text)
            if m:
                matched = m.variables()
            else:
                print('Invalid command\n')
                continue

            if matched.get('operator1') or matched.get('operator2'):
                try:
                    var1 = float(matched.get('var1', 0))
                    var2 = float(matched.get('var2', 0))
                except ValueError:
                    print('Invalid command (2)\n')
                    continue

                # Turn the operator string into a function.
                operator = {
                    'add': (lambda a, b: a + b),
                    'sub': (lambda a, b: a - b),
                    'mul': (lambda a, b: a * b),
                    'div': (lambda a, b: a / b),
                    'sin': (lambda a, b: math.sin(a)),
                    'cos': (lambda a, b: math.cos(a)),
                }[matched.get('operator1') or matched.get('operator2')]

                # Execute and print the result.
                print('Result: %s\n' % (operator(var1, var2)))

            elif matched.get('operator2'):
                print('Operator 2')

    except EOFError:
        pass
