import ipaddress
import socket
from common import *
from exceptions import *

def read_socket(socket, numbytes):
    try:        
        data = b''        
        # return socket.recv(1000)
        while len(data) < numbytes:           
            data += socket.recv(numbytes)              
            if len(data) == 0:
                raise SocketClosedByPeer('read_socket: data=%s' % data)
        return data
    except OSError as msg:
        print('read_socket] Error whilst reading %d bytes' % numbytes)
        print('  %s bytes in buffer: %s "%s"' % (len(data), hexlify(data), data))
        print(msg)
        return None


def parse_ipv6(data):
    if len(data) != 16:
        raise ParseErrorBadIPv6()
    return ipaddress.IPv6Address(data)



