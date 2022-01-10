#!/usr/bin/env python
# -*- Mode: Python; tab-width: 4 -*-
#
# iMilestone
#
# Copyright (C) 2011 Marco Lertora <marco.lertora@infoporto.it>
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

from types import StringType, IntType, BooleanType
from dataview import DataView
from uuid import UUID
from lxml import etree

class XPMOBILE(object):

    class InvalidPacket(Exception):
        pass

    class IncompletePacket(Exception):
        pass

    class PROTOCOL:
        HTTP = 'HTTP'

    class VIEW:
        ROOT = '1926418b-893e-4ad6-a258-fb4a9ab57453'
        ALLCAMERA = 'bb16cc8f-a2c5-44f8-9d20-6e9ac57806f5'

    class COMMAND:
        LOGIN = 'LogIn'
        CONNECT = 'Connect'
        DISCONNECT = 'Disconnect'
        LIVEMESSAGE = 'LiveMessage'
        GETVIEWS = 'GetViews'
        REQUESTSTREAM = 'RequestStream'
        CLOSESTREAM = 'CloseStream'

    class METHODTYPE:
        PUSH = 'Push'
        PULL = 'Pull'

    class SIGNALTYPE:
        LIVE = 'Live'
        UPLOAD = 'Upload'
        PLAYBACK = 'Playback'

    class STREAMTYPE:
        NATIVE = 'Native'
        TRANSCODED = 'Transcoded'

    class BYTEORDER:
        BIGENDIAN = 'BigEndian'
        LITTLEENDIAN = 'LittleEndian'

    class CODE:
        EOP = '\r\n\r\n'
        EOL = '\r\n'
        NULL = '\x00'

    class NS:
        XSI = 'http://www.w3.org/2001/XMLSchema-instance'
        XSD = 'http://www.w3.org/2001/XMLSchema'

    class HEADERFLAG:
        SIZE = 0x01
        LIVE = 0x02
        PLAYBACK = 0x04

    @staticmethod
    def connect(sequenceId, publicKey=None):
        commandParams = dict()
        if publicKey is not None: commandParams['PublicKey'] = publicKey
        return XPMOBILE.buildPacket(sequenceId, XPMOBILE.COMMAND.CONNECT, commandParams)

    @staticmethod
    def disconnect(sequenceId, connectionId):
        commandParams = dict()
        return XPMOBILE.buildPacket(sequenceId, XPMOBILE.COMMAND.DISCONNECT, commandParams, connectionId)

    @staticmethod
    def liveMessage(sequenceId, connectionId):
        commandParams = dict()
        return XPMOBILE.buildPacket(sequenceId, XPMOBILE.COMMAND.LIVEMESSAGE, commandParams, connectionId)

    @staticmethod
    def logIn(sequenceId, connectionId, username, password):
        commandParams = dict()
        commandParams['Username'] = username
        commandParams['Password'] = password
        return XPMOBILE.buildPacket(sequenceId, XPMOBILE.COMMAND.LOGIN, commandParams, connectionId)

    @staticmethod
    def getViews(sequenceId, connectionId, viewId):
        commandParams = dict()
        commandParams['ViewId'] = viewId
        return XPMOBILE.buildPacket(sequenceId, XPMOBILE.COMMAND.GETVIEWS, commandParams, connectionId)

    @staticmethod
    def requestStream(sequenceId, connectionId, cameraId, methodType, streamResolution, streamCompression=70, streamFPS=10):
        streamWidth, streamHeight = streamResolution
        commandParams = dict()
        commandParams['CameraId'] = cameraId
        commandParams['SignalType'] = XPMOBILE.SIGNALTYPE.LIVE
        commandParams['StreamType'] = XPMOBILE.STREAMTYPE.TRANSCODED
        commandParams['KeyFramesOnly'] = False
        commandParams['MethodType'] = methodType
        commandParams['DestWidth'] = streamWidth
        commandParams['DestHeight'] = streamHeight
        commandParams['ComprLevel'] = streamCompression
        commandParams['Fps'] = streamFPS
        return XPMOBILE.buildPacket(sequenceId, XPMOBILE.COMMAND.REQUESTSTREAM, commandParams, connectionId)


    @staticmethod
    def requestStreamUpload(sequenceId, connectionId, methodType):
        commandParams = dict()
        commandParams['SignalType'] = XPMOBILE.SIGNALTYPE.UPLOAD
        commandParams['StreamType'] = XPMOBILE.STREAMTYPE.TRANSCODED
        commandParams['MethodType'] = methodType
        return XPMOBILE.buildPacket(sequenceId, XPMOBILE.COMMAND.REQUESTSTREAM, commandParams, connectionId)


    @staticmethod
    def closeStream(sequenceId, connectionId, videoId):
        commandParams = dict()
        commandParams['VideoId'] = videoId
        return XPMOBILE.buildPacket(sequenceId, XPMOBILE.COMMAND.CLOSESTREAM, commandParams, connectionId)

    @staticmethod
    def buildPacket(sequenceId, commandName, commandParams=None, connectionId=None):
        commandType = 'Request'
        commandParams = commandParams if commandParams is not None else dict()
        xmlCommunication = etree.Element('Communication', nsmap=dict(xsi=XPMOBILE.NS.XSI, xsd=XPMOBILE.NS.XSD))
        if connectionId is not None: etree.SubElement(xmlCommunication, 'ConnectionId').text = connectionId
        xmlCommand = etree.SubElement(xmlCommunication, 'Command')
        if sequenceId is not None: xmlCommand.attrib['SequenceId'] = str(sequenceId)
        etree.SubElement(xmlCommand, 'Type').text = commandType
        etree.SubElement(xmlCommand, 'Name').text = commandName
        xmlCommandParams = etree.SubElement(xmlCommand, 'InputParams')
        for paramKey, paramValue in commandParams.items():
            if type(paramValue) == IntType: paramValue = str(paramValue)
            elif type(paramValue) == BooleanType: paramValue = 'YES' if paramValue else 'NO'
            elif type(paramValue) == StringType: pass
            else: assert False, 'Invalid type %r' % (type(paramValue))
            etree.SubElement(xmlCommandParams, 'Param', Name=paramKey, Value=paramValue)
        payload = etree.tostring(xmlCommunication, pretty_print=False, encoding='utf-8', xml_declaration=True)
        return payload + XPMOBILE.CODE.EOP

    @staticmethod
    def convertUUID(uuid):
        data = str()
        for index in range(16):
            data = data + uuid.bytes[[3,2,1,0,5,4,7,6,8,9,10,11,12,13,14,15][index]]
        return data

    @staticmethod
    def buildFrame(videoId, frameData, byteOrder):
        headerLength = 36
        dataView = DataView() 
        dataView.writeString(XPMOBILE.convertUUID(UUID(videoId)))
        dataView.writeChar(XPMOBILE.CODE.NULL, 12)
        dataView.writeUInteger(len(frameData))
        dataView.writeUShort(headerLength)       
        dataView.writeChar(XPMOBILE.CODE.NULL, 2)
        return dataView.toData() + frameData

    @staticmethod
    def parseFrame(videoId, videoData, byteOrder):
        values = dict()

        try:
            dataView = DataView(videoData) 
            values['VideoId'] = dataView.readUUID()
            values['Timestamp'] = dataView.readTimestamp()
            values['FrameNumber'] = dataView.readUInteger()
            values['FrameSize'] = dataView.readUInteger()
            values['HeaderSize'] = dataView.readUShort()
            values['HeaderFlags'] = dataView.readUShort()
            if not values['HeaderSize']: values['HeaderSize'] = dataView.readUInteger()
        
            if values['HeaderFlags'] & XPMOBILE.HEADERFLAG.SIZE:
                values['SourceSize'] = (dataView.readUInteger(), dataView.readUInteger())
                values['SourceCrop'] = (dataView.readUInteger(), dataView.readUInteger(), dataView.readUInteger(), dataView.readUInteger())
                values['DestinationSize'] = (dataView.readUInteger(), dataView.readUInteger())
                values['DestinationCrop'] = (dataView.readUInteger(), dataView.readUInteger(), dataView.readUInteger(), dataView.readUInteger())

            if values['HeaderFlags'] & XPMOBILE.HEADERFLAG.LIVE:
                values['CurrentLiveEvents'] = dataView.readUInteger()
                values['ChangedLiveEvents'] = dataView.readUInteger()

            if values['HeaderFlags'] & XPMOBILE.HEADERFLAG.PLAYBACK:
                values['CurrentPlaybackEvents'] = dataView.readUInteger()
                values['ChangedPlaybackEvents'] = dataView.readUInteger()

            values['FrameBytes'] = dataView.readString(values['FrameSize'])
            trail = dataView.readAll()

        except DataView.IncompletePacket, e:
            raise XPMOBILE.IncompletePacket()

        return values, trail
 
    @staticmethod
    def parsePacket(data):
        xmlRoot = etree.fromstring(data)
        sequenceId = xmlRoot.xpath('/Communication/Command/@SequenceId').pop()
        commandType = xmlRoot.xpath('/Communication/Command/Type/text()').pop()
        commandName = xmlRoot.xpath('/Communication/Command/Name/text()').pop()
        commandSubItems = dict()
        for item in xmlRoot.xpath('/Communication/Command/SubItems/Item'):
            commandSubItems[item.attrib['Id']] = dict(item.attrib)
        commandInputParams, commandOutputParams = dict(), dict()
        for param in xmlRoot.xpath('/Communication/Command/InputParams/Param'):
            commandInputParams[param.attrib['Name']] = param.attrib['Value']
        for param in xmlRoot.xpath('/Communication/Command/OutputParams/Param'):
            commandOutputParams[param.attrib['Name']] = param.attrib['Value']
        commandResult = xmlRoot.xpath('/Communication/Command/Result/text()').pop()
        xmlCommandErrorCode = xmlRoot.xpath('/Communication/Command/ErrorCode/text()')
        commandErrorCode = xmlCommandErrorCode.pop() if xmlCommandErrorCode else None
        xmlCommandErrorString = xmlRoot.xpath('/Communication/Command/ErrorString/text()')
        commandErrorString = xmlCommandErrorString.pop() if xmlCommandErrorString else None

        logs = list()
        values = commandOutputParams
        values['SubItems'] = commandSubItems
        if commandResult == 'Error': logs.append('Error code: %r %r' % (commandErrorCode, commandErrorString))
        return int(sequenceId), commandName, values, logs

if __name__ == '__main__':
    import httplib
    import sys

    DEVEL = True
    port = 8081
    hostname = '172.16.2.11'
    videoUrl = '/XProtectMobile/Video'
    communicationUrl = '/XProtectMobile/Communication'

    def parseFrame(filename):
        fin = open(filename, 'rb')
        videoData = fin.read()
        fin.close()
        videoId = 0
        byteOrder = XPMOBILE.BYTEORDER.LITTLEENDIAN
        frameData = XPMOBILE.parseFrame(videoId, videoData, byteOrder)

    def request(body):
        con = httplib.HTTPConnection(hostname, port, timeout=10)
        if DEVEL: con.set_debuglevel(200)
        headers = dict()
        headers['Content-type'] = 'text/xml'
        con.request('POST', communicationUrl, body, headers)
        response = con.getresponse()
        if DEVEL: print 'response:', response.status, response.reason
        data = response.read()
        if DEVEL: print 'response: data size', len(data)
        packet = XPMOBILE.parsePacket(data)
        con.close()
        return packet 

    def requestVideo(videoId, byteOrder):
        con = httplib.HTTPConnection(hostname, port, timeout=10)
        if DEVEL: con.set_debuglevel(200)
        body = None
        headers = dict()
        headers['Content-type'] = 'text/xml'
        headers['Content-Lenght'] = '0'
        url = '%s/%s' % (videoUrl, videoId)
        con.request('GET', url, body, headers)
        response = con.getresponse()
        if DEVEL: print 'response:', response.status, response.reason
        while True: 
            frame = XPMOBILE.parseFrame(videoId, response, byteOrder)
            if frame: dump(videoId + '-' + str(i), frame)
            con.close()

    def dump(videoId, videoData):
        print 'dump frame: %s' % (videoId)
        basepath = 'out'
        filename = '%s/%s' % (basepath, videoId) 
        fout = open(filename, 'wb')
        fout.write(videoData)
        fout.close()

    sequenceId = 1
    publicKey = None
    username, password = 'admin', 'admin'

    op, values, logs = request(XPMOBILE.connect(sequenceId, publicKey))
    connectionId = values['ConnectionId']
    op, values, logs = request(XPMOBILE.liveMessage(sequenceId, connectionId))
    op, values, logs = request(XPMOBILE.logIn(sequenceId, connectionId, username, password))
    viewId = '1926418b-893e-4ad6-a258-fb4a9ab57453'
    viewId = 'bb16cc8f-a2c5-44f8-9d20-6e9ac57806f5'
    op, values, logs = request(XPMOBILE.getViews(sequenceId, connectionId, viewId))
    cameraId = 'adb1b363-4224-4dd5-87b0-5fe1fa768dc2'
    for i in range(1):
        op, values, logs = request(XPMOBILE.requestStream(sequenceId, connectionId, cameraId))
        videoId = values['VideoId']
        streamId = values['StreamId']
        for i in range(10000):
            byteOrder = values['ByteOrder']
            videoData = requestVideo(videoId, byteOrder)

    op, values, logs = request(XPMOBILE.disconnect(sequenceId, connectionId))
