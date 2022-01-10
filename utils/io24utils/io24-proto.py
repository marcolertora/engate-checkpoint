import time
from struct import pack


cmds = {
    'identify' : { 'nargs': 0, 'cmd': 'IO24' },
    }

rply = {
    'IO24': ( { 'name': 'mac', 'len': 6, 'conv': 'bytes' } ),
    }


def ip2ee(ip):
    p = ip.split('.')
    (a, b, c, d) = map(int, p)
    return (chr(b) + chr(a), chr(d) + chr(c))

def hex2str_p(bytes):
    return ' '.join(map(lambda x: '0x%02x' % ord(x), bytes))

if __name__ == '__main__':
    #(a, b) = ip2ee('192.168.69.69')
    #(a, b) = ip2ee('10.0.0.100')
    #print hex2str_p(a), hex2str_p(b)
    #raise SystemExit
    from socket import * 
    s = socket(AF_INET, SOCK_DGRAM)
    #addr =  ('192.168.69.146', 2424)
    #addr =  ('192.168.255.80', 2424)
    addr = ('io001', 2424)
    #s.sendto('IO24', ('192.168.69.146', 2424))
    #s.sendto('!A\xff', addr) # all input
    #s.sendto('!A\x06', addr) # all output
    #s.sendto('!B\x00', addr) # all output
    #s.sendto('!C\x00', addr) # all output
    #raise SystemExit

    #(a, b) = ip2ee('192.168.69.80')

    s.sendto('A\x40', addr)
    #s.sendto('B\xff', addr)
    #s.sendto('C\xff', addr))

    time.sleep(0.1)

    s.sendto('A\x00', addr)
    #s.sendto('B\x00', addr)
    #s.sendto('C\x00', addr)

    # 11011111
    #s.sendto("'1\x05\xaa\x55", addr)
    #s.sendto("'W\x05\xff\xdf", addr)
    #s.sendto("'W\x05\xff\xfb", addr)
    #s.sendto("'W\x05\xff\xff", addr)
    #s.sendto("'0\x05\x00\x00", addr)

    #s.sendto("'1\x06\xaa\x55", addr)
    #s.sendto("'W\x06" + a, addr)
    #s.sendto("'0\x06\x00\x00", addr)

    #s.sendto("'1\x07\xaa\x55", addr)
    #s.sendto("'W\x07" + b, addr)
    #s.sendto("'0\x07\x00\x00", addr)

    # mask
    #s.sendto("'1\x20\xaa\x55", addr)
    #s.sendto("'W\x20\x00\xff", addr)
    #s.sendto("'0\x20\x00\x00", addr)

    # port
    #p = pack('!H', 2424)
    #s.sendto("'1\x1d\xaa\x55", addr)
    #s.sendto("'W\x1d" + p, addr)
    #s.sendto("'0\x1d\x00\x00", addr)

    #s.sendto("'@\x00\xaa\x55", addr)

    #s.sendto("'R\x05\x00\x00", addr)
    #print hex2str_p(s.recv(4))

    raise SystemExit

    #s.sendto('#A\xff', addr) # 1.4
    #s.sendto('@A\xff', addr) # 1.4
    
    while 1:
        s.sendto('a', addr)
        data = s.recv(8)
        print hex2str_p(data)
        time.sleep(1)
