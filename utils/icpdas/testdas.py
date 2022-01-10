#  gcc -shared -o libUSBIO_python.so libUSBIO_arm.so.1.0 -lgcc_s

from ctypes import *
from time import sleep


def prettyPrint(numofport, portvalue):
    for port in range(numofport):
        value = (portvalue >> port) & 0x01
        print "USB-2064 Port %d Value %d" % (port, value)


lib = cdll.LoadLibrary('./libUSBIO_python.so')

res = lib.USBIO_GetLibraryVersion()
print "USB I/O Library Version : %s" % c_char_p(res).value

devid = c_int()
boardid = c_ubyte(1)
res = lib.USBIO_OpenDevice(boardid, byref(devid))
print "USB-2060 Opening Device: %d" % devid.value

if res:
    print 'Errore %d' % res
    raise SystemExit

userboardid = c_ubyte(126)
lib.USBIO_SetUserDefinedBoardID(devid, userboardid)

#get number of DO and DI
numofdo = c_ubyte()
numofdi = c_ubyte()
lib.USBIO_GetDOTotal(devid, byref(numofdo))
lib.USBIO_GetDITotal(devid, byref(numofdi))
print "USB-2060 DO Number: %d" % numofdo.value
print "USB-2060 DI Number: %d" % numofdi.value

sleep(1)

#read and write DO value
dowvalue = c_ubyte(0x18)
dorvalue = c_ubyte()
lib.USBIO_DO_WriteValue(devid, byref(dowvalue))
print "USB-2060 DO Write Value: 0x%X" % dowvalue.value
lib.USBIO_DO_ReadValue(devid, byref(dorvalue))
print "USB-2064 DO Read Value: 0x%X" % dorvalue.value
prettyPrint(numofdo.value, dorvalue.value)

sleep(1)

do_value =  c_ubyte()
do_conf = c_ubyte()

dirvalue = c_ubyte()
lib.USBIO_DI_ReadValue(devid, byref(dirvalue))
print "USB-2064 DI Read Value: 0x%X" % dirvalue.value
prettyPrint(numofdi.value, dirvalue.value)

res = lib.USBIO_CloseDevice(devid)
if res:
    print 'Errore %d' % res
    raise SystemExit
