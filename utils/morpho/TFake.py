#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements. See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership. The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License. You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied. See the License for the
# specific language governing permissions and limitations
# under the License.
#

from thrift.transport import TTransport

class TFake(TTransport.TTransportBase):
  """Base class for Thrift transport layer."""

  pippo = ''

  def isOpen(self):
    pass

  def open(self):
    pass

  def close(self):
    pass

  def read(self, sz):
    return ''

  def write(self, buf):
    print '>>>>>', buf.encode('hex')
    self.pippo += buf
    print '>>>>>', repr(buf)

  def flush(self):
    print 'flush', self.pippo.encode('hex')
    pass
