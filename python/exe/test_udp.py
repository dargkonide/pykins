import socket
from random import choice

socks=[]
for n in range(1000):
    socks.append(socket.socket(socket.AF_INET,socket.SOCK_DGRAM))
for n in range(1000):
    choice(socks).sendto(b'test',('10.106.145.172',1234))
