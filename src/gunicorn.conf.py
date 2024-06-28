import multiprocessing
import socket
import fcntl
import struct

def get_ip_address(ifname): 
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
    return socket.inet_ntoa(fcntl.ioctl( 
        s.fileno(),
        0x8915,
        struct.pack('256s', bytes(ifname[:15], 'utf-8')) 
    )[20:24])

ip_address = get_ip_address('eth0')

build = f"{ip_address}:8000"
#build = "0.0.0.0:8000"
workers = multiprocessing.cpu_count() * 2 + 1

timeout = 30
preload = True
loglevel = "debug"