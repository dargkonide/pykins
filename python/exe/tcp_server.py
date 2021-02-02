from socket import socket

s=socket()
s.bind(('',4321))
s.listen(1)

while 1:
    print(s.accept())