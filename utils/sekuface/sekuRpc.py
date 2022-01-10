'''
Created on 11/mar/2013

@author: Andrea
'''
from twisted.web import xmlrpc
from twisted.internet import reactor
from twisted.web import server

from xmlrpclib import Fault, Binary
import random
from os import path
from pickle import loads, dumps

class XmlRpcService(xmlrpc.XMLRPC):

    @staticmethod
    def readAndAnswer(*args, **kargs):
        filename = 'response.py'

        def response(*args, **kargs):
            return kargs['defaultResponse']

        if path.exists(filename):
            exec(open(filename, 'rb').read())

        try: res = response(*args, **kargs)
        except Exception, e: raise Fault(10, repr(e))
        return res


    def xmlrpc_enrollBiometric(self, stringName):
        """Avvia la procedura di acquisizione del SF. Ritorna la biometrica e la foto acquisita."""
        print 'enrollBiometric params: %s' % (stringName)

        try:
            response = dict()
            response['imageStream'] = Binary(open('face.jpg', 'rb').read())
            response['bioTemplate'] = Binary(open('face.jpg', 'rb').read())
            response['imageContentType'] = 'image/jpeg'
            return XmlRpcService.readAndAnswer('enrollBiometric', defaultResponse=response)
        except:
            raise Fault(102, 'Problema Hardware')

    def xmlrpc_verifyBiometric(self, binaryBioTemplate, stringName):
        """Avvia verifica sul SF. ritorna l'immagine acquisita e il punteggio ottenuto"""
        print "Verify Biometric: received template: %r " % binaryBioTemplate.data

        try:
            response = dict()
            response['score'] = random.random() # compreso fra 0 e 1
            response['imageStream'] = Binary(open('face.jpg', 'rb').read())
            response['imageContentType'] = 'image/jpeg'
            print "Verify Biometric: score: %r" % (response['score'])
            return XmlRpcService.readAndAnswer('verifyBiometric', defaultResponse=response)
        except:
            raise Fault(102, 'Problema Hardware')


    def xmlrpc_showMessage(self, stringMessage, stringColor):
        """Mostra un messaggio sul SF"""
        print 'showMessage params: %s %s' % (stringMessage, stringColor)

        try:
            return XmlRpcService.readAndAnswer('verifyBiometric', defaultResponse=True)
        except:
            raise Fault(102, 'Problema Hardware')


    def xmlrpc_getStatus(self):
        """Chiede lo stato del SF"""

        print 'getStatus'
        try:
            response = dict()
            response['version'] = 'SF Ver. 1.0'
            response['status'] = 'OK' #, 'WARNING', 'ERROR'][random.randrange(3)]
            return XmlRpcService.readAndAnswer('verifyBiometric', defaultResponse=response)
        except:
            raise Fault(102, 'Problema Hardware')


if __name__ == '__main__':
    listenport = 9988
    print 'listen on %d' % (listenport)
    s = XmlRpcService(allowNone=True, useDateTime=True)
    reactor.listenTCP(listenport, server.Site(s))
    reactor.run()
