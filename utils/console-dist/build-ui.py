#!/usr/bin/env python
# -*- Mode: Python; tab-width: 4 -*-
#
# Software Controllo Accessi
#
# Copyright (c) 2010-2011 Netfarm S.r.l.
# Gianluigi Tiesi <sherpya@netfarm.it>
# Alfredo Oliviero <alfredo.oliviero@netfarm.it>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTIBILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# for more details.
# ======================================================================

import sys
import os
from pysideuic.driver import Driver
from pysideuic.port_v2.invoke import invoke
from optparse import Values

def make_opt(output):
    return Values(dict(execute=False, from_imports=False, indent=4, debug=False, preview=False, output=output))

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'Impara!'
        raise SystemExit

    if sys.argv[1] == '-rc':
        if sys.platform == 'win32':
            import PySide
            pyside_rcc = os.path.join(PySide.__path__[0], 'pyside-rcc.exe')
        else:
            pyside_rcc = 'pyside-rcc'
        cmd = '%s -o console_rc.py console.qrc' % pyside_rcc
        os.system(cmd)
        print 'Resources compiled'
        raise SystemExit

    for ui in sys.argv[1:]:
        opts = make_opt(ui + '.py')
        try:
            invoke(Driver(opts, ui + '.ui'))
        except Exception, e:
            print e
            continue
        print 'Compiled', ui
