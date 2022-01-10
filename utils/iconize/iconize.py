import sys
import xmlrpclib
from pprint import pprint 
import time
import types

# fix null: ex:nil tag same as nil
#def dump_nil (self, value, write):
#    if not self.allow_none: raise TypeError, 'cannot marshal None unless allow_none is enabled'
#    write('<value xmlns:ex="http://ws.apache.org/xmlrpc/namespaces/extensions"><ex:nil/></value>')

#mlrpclib.Marshaller.dispatch[types.NoneType] = dump_nil
xmlrpclib.Unmarshaller.dispatch['ex:u8'] = xmlrpclib.Unmarshaller.end_int

DEBUG = False

if __name__ == '__main__':
    endpoint = 'http://10.20.107.66:11111'
    authorityID = '430a353b51954037e3ce0cfe'
    accessUserDatasEncrypted = False
    accessUserName = 'demo'
    accessUserPassword = 'demo'

    def pool(num, sleep=1):
        for i in range(num):
            ret = s.PalmSecureGetProcessingState()
            print(ret)
            time.sleep(sleep)

    if 0:
        url = '%s/IC_CREDENTIAL_MANAGER_PROCESS_DAEMON/rpc/credential_manager/' % endpoint
        s = xmlrpclib.Server(url, verbose=DEBUG)
        credentials = s.CredentialManagerGetCredentialList(authorityID, accessUserDatasEncrypted, accessUserName, accessUserPassword)
        for credential in credentials:
            print credential['item_id'], credential['ic__comp'], credential['ic__foren'], credential['ic__surn']
            credentialID = credential['item_id']
            if 0:
                dcredential = s.CredentialManagerGetCredentialDetails(authorityID, credentialID, accessUserDatasEncrypted, accessUserName, accessUserPassword)
                print dcredential['item_id'], dcredential['ic__comp'], dcredential['ic__foren'], dcredential['ic__surn']

    if 1:
        url = '%s/IC_DEVICE_POOL_PROCESS_DAEMON/rpc/device_pool' % endpoint
        s = xmlrpclib.Server(url, verbose=DEBUG)
        ret = s.GetDeviceList()
        pprint(ret)


    if 1:
        url = '%s/IC_PALMSECURE1_PROCESS_DAEMON/rpc/palmsecure_base/' % endpoint
        s = xmlrpclib.Server(url, verbose=DEBUG)
        paramA = {  'EncryptionDataType'        : 3,
                    'GuideMode'                 : 0,
                    'ImmediateStore'            : False,
                    'MaximumSplitTemplateSize'  : 0,
                    'RegisterDataType'          : 1,
                    'SensorDirection'           : 0,
                    'TemplateActions'           : [],
                    'TemplateComment'           : 'TemplateComment',
                    'TemplateHandType'          : 'IC_PALM_SECURE_BASE_HAND_TYPE_LEFT_PALM',
                    'TemplateName'              : 'WEB CONFIG TEMPLATE:lefthand User:Sperandeo',
                    'UserID'                    : 'cUm3PfHiNPm-ET0ULmxT79VJDaDSoe0SoEd3K_lkrm2QXjv9-1d5Q99Cp7zoIoYFhuFQl7bGW0O31fa4SlzlIA==',
                 }
                
        pool(10)
        paramB = 0
        paramC = ['*']
        ret = s.PalmSecureEnrollTemplate(authorityID, paramA, paramB, paramC, accessUserDatasEncrypted, accessUserName, accessUserPassword)
        pprint(ret)
        pool(100)
