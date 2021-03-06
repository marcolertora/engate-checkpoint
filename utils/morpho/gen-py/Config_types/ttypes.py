#
# Autogenerated by Thrift Compiler (0.9.1)
#
# DO NOT EDIT UNLESS YOU ARE SURE THAT YOU KNOW WHAT YOU ARE DOING
#
#  options string: py
#

from thrift.Thrift import TType, TMessageType, TException, TApplicationException
import Generic_types.ttypes


from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol, TProtocol
try:
  from thrift.protocol import fastbinary
except:
  fastbinary = None



class Config_inexistent_parameter_error(TException):
  """
  The requested parameter does not exist in terminal configuration database.

  Attributes:
   - err_code
   - parameter_name_UTF8
  """

  thrift_spec = (
    None, # 0
    (1, TType.I32, 'err_code', None, None, ), # 1
    (2, TType.STRING, 'parameter_name_UTF8', None, None, ), # 2
  )

  def __init__(self, err_code=None, parameter_name_UTF8=None,):
    self.err_code = err_code
    self.parameter_name_UTF8 = parameter_name_UTF8

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      if fid == 1:
        if ftype == TType.I32:
          self.err_code = iprot.readI32();
        else:
          iprot.skip(ftype)
      elif fid == 2:
        if ftype == TType.STRING:
          self.parameter_name_UTF8 = iprot.readString();
        else:
          iprot.skip(ftype)
      else:
        iprot.skip(ftype)
      iprot.readFieldEnd()
    iprot.readStructEnd()

  def write(self, oprot):
    if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
      oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
      return
    oprot.writeStructBegin('Config_inexistent_parameter_error')
    if self.err_code is not None:
      oprot.writeFieldBegin('err_code', TType.I32, 1)
      oprot.writeI32(self.err_code)
      oprot.writeFieldEnd()
    if self.parameter_name_UTF8 is not None:
      oprot.writeFieldBegin('parameter_name_UTF8', TType.STRING, 2)
      oprot.writeString(self.parameter_name_UTF8)
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()

  def validate(self):
    if self.err_code is None:
      raise TProtocol.TProtocolException(message='Required field err_code is unset!')
    if self.parameter_name_UTF8 is None:
      raise TProtocol.TProtocolException(message='Required field parameter_name_UTF8 is unset!')
    return


  def __str__(self):
    return repr(self)

  def __repr__(self):
    L = ['%s=%r' % (key, value)
      for key, value in self.__dict__.iteritems()]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

  def __ne__(self, other):
    return not (self == other)

class Config_invalid_value_error(TException):
  """
  The specified value for the requested parameter is invalid.

  Attributes:
   - err_code
   - parameter_name_UTF8
  """

  thrift_spec = (
    None, # 0
    (1, TType.I32, 'err_code', None, None, ), # 1
    (2, TType.STRING, 'parameter_name_UTF8', None, None, ), # 2
  )

  def __init__(self, err_code=None, parameter_name_UTF8=None,):
    self.err_code = err_code
    self.parameter_name_UTF8 = parameter_name_UTF8

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      if fid == 1:
        if ftype == TType.I32:
          self.err_code = iprot.readI32();
        else:
          iprot.skip(ftype)
      elif fid == 2:
        if ftype == TType.STRING:
          self.parameter_name_UTF8 = iprot.readString();
        else:
          iprot.skip(ftype)
      else:
        iprot.skip(ftype)
      iprot.readFieldEnd()
    iprot.readStructEnd()

  def write(self, oprot):
    if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
      oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
      return
    oprot.writeStructBegin('Config_invalid_value_error')
    if self.err_code is not None:
      oprot.writeFieldBegin('err_code', TType.I32, 1)
      oprot.writeI32(self.err_code)
      oprot.writeFieldEnd()
    if self.parameter_name_UTF8 is not None:
      oprot.writeFieldBegin('parameter_name_UTF8', TType.STRING, 2)
      oprot.writeString(self.parameter_name_UTF8)
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()

  def validate(self):
    if self.err_code is None:
      raise TProtocol.TProtocolException(message='Required field err_code is unset!')
    if self.parameter_name_UTF8 is None:
      raise TProtocol.TProtocolException(message='Required field parameter_name_UTF8 is unset!')
    return


  def __str__(self):
    return repr(self)

  def __repr__(self):
    L = ['%s=%r' % (key, value)
      for key, value in self.__dict__.iteritems()]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

  def __ne__(self, other):
    return not (self == other)
