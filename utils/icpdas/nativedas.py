import usb
import sys
import os
import time


class ICPDas2060():
    VENDOR_ID = 0x1b5c  #: Vendor Id
    PRODUCT_ID = 0x043c  #: Product Id for the bridged usb cable
    INTERFACE_ID = 0  #: The interface we use to talk to the device
    INTERRUPT_IN_EP = 0x81  #: Endpoint for Bulk reads
    PACKET_LENGTH = 0x40  #: 64 bytes
    CMD_READ_INPUT_STATUS = [0x0, 0x0,0x0, 0x0, 0x10, 0x48,0,0,0,0,0]
    CMD_READ_RL_STATUS = [0x0, 0x0, 0x0, 0x0, 0x10, 0x40,0,0,0,0,0]
    CMD_PREFIX_SET_POWERON_RL_STATUS = [0x10, 0, 0x06, 0, 0, 0x40, 0x06, 0x00, 0, 0]
    CMD_PREFIX_SET_RL_STATUS = [0x10, 0, 0x01, 0, 0x10, 0x40, 0x01, 0, 0, 0]

    def __init__(self, vendor_id=VENDOR_ID, product_id=PRODUCT_ID):
        self.busses = usb.busses()  # enumerate busses
        self.handle = None
        self.device = None
        try:
            for bus in self.busses:
                devices = bus.devices
                for dev in devices:
                    if dev.idVendor == vendor_id and dev.idProduct == product_id:  # device matches
                        self.device = dev
                        self.conf = self.device.configurations[0]
                        self.intf = self.conf.interfaces[0][0]
                        self.endpoints = []
                        for endpoint in self.intf.endpoints:
                            self.endpoints.append(endpoint)

            if self.device is None:
                raise ValueError('Device not found')
        except Exception, err:
            print >> sys.stderr, err
            raise ValueError('Device not found')

    def get_device(self):
        return self.device

    def open(self):
        if self.handle:
            self.handle = None
        try:
            self.handle = self.device.open()
            if self.device.dev.is_kernel_driver_active(0):
              self.device.dev.detach_kernel_driver(0)
           # self.handle.detachKernelDriver(self.intf)
            self.handle.setConfiguration(self.conf)
            self.handle.claimInterface(self.intf)
            self.handle.setAltInterface(self.intf)
            return True
        except usb.USBError, err:
            print >> sys.stderr, err
            return False

    def close(self):
        """ Release device interface """
        try:
           # self.handle.reset()
            self.handle.releaseInterface()
            if not self.device.dev.is_kernel_driver_active(0):
             self.device.dev.attach_kernel_driver(0)

        except Exception, err:
            print >> sys.stderr, err
        self.handle, self.device = None, None


    def write(self, ep, buff, timeout=100):
        try:
            return self.handle.interruptWrite(ep, buff, timeout)  # return bytes written
        except:
            return 0


    def read(self, ep, size, timeout=100):
        try:
            return self.handle.interruptRead(ep, size, timeout)  # return data read
        except:
            return []

    def setReport(self, data, timeout=500):
        try:

            sent_bytes = self.handle.controlMsg(0x21, 0x09, data, 0x200, 0, timeout)
           # time.sleep(1)
            if sent_bytes:
                read_bytes = self.read(self.INTERRUPT_IN_EP, self.PACKET_LENGTH, timeout);
            return read_bytes[1:len(data)] == data[1:len(data)]


        except Exception, err:
            print >> sys.stderr, err
            return 0


    def getReport(self, data, timeout=1000):
        try:
            sent_bytes = self.handle.controlMsg(0x21, 0x09, data, 0x200, 0, timeout)
	    time.sleep(1)
            if sent_bytes:
                read_bytes = self.read(self.INTERRUPT_IN_EP, self.PACKET_LENGTH, timeout);
                return read_bytes


        except Exception, err:
            print >> sys.stderr, err
            return 0


    def read_inputs_status(self):
        res = self.getReport(self.CMD_READ_INPUT_STATUS,5000)
        return bin(res[10])[2:].zfill(8)


    def read_rl_status(self):
        res = self.getReport(self.CMD_READ_RL_STATUS,5000)
        return bin(res[10])[2:].zfill(8)

    def setPowerOnRL(self,hexArray):
            return self.setReport(self.CMD_PREFIX_SET_POWERON_RL_STATUS + hexArray)


    def setRelayStatus(self, rlNumber):
        '''
            rlNumber e' il numero hex corrispondente al bitarray che setta i relays:
                es:
                 set RL0 : 00000001 -> 0x01
                 set RL0 e RL2 : 00000101 -> 0x01+0x04

        '''

        msg = self.CMD_PREFIX_SET_RL_STATUS + [rlNumber]
        return self.setReport(msg,5000)


    def getDeviceName(self):
        return self.handle.getString(2, 40)


if __name__ == '__main__':
    icp = ICPDas2060()
    icp.open()
    icp.setRelayStatus(1)
    print "Relays Status: ", icp.read_rl_status()
    time.sleep(1)
    icp.setPowerOnRL([0,0,0,0,0])
    icp.setRelayStatus(0)
    print "Inputs Status: ", icp.read_inputs_status()
    print "Relays Status: ", icp.read_rl_status()
    icp.close()