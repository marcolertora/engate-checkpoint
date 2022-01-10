#!/usr/bin/env python
# -*- Mode: Python; tab-width: 4 -*-
#
# Software Controllo Accessi
#
# Copyright (c) 2010 Netfarm S.r.l.
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

q = """
DROP TABLE c_io24_entry;

CREATE TABLE c_io24_entry
(
  id_io24_entry serial NOT NULL,
  id_reader integer NOT NULL,
  id_checkpoint integer NOT NULL,
  porta character(1) NOT NULL,
  linea integer NOT NULL,
  direction boolean NOT NULL,
  enabled boolean NOT NULL DEFAULT true,
  note character varying(1024),
  timer double precision,
  CONSTRAINT io24_pkey PRIMARY KEY (id_io24_entry)
)
"""

#protocollo dell'apriporta
from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor

class IO24test(DatagramProtocol):
    def __init__(self, callback):
        self.callback = callback

    def datagramReceived(self, d, host):
        print repr(d)
        if len(d) != 3:
            print "io24, ricevuto messaggio di dimensione sbagliata", len(d)
            return

        port = bool(ord(d[2]) & 1)
        self.callback(port)

def debug(arg):
    print 'received', arg

def main():
    protocol = IO24test(debug)
    t = reactor.listenUDP(2424, protocol)
    reactor.run()

if __name__ == '__main__':
    main()
