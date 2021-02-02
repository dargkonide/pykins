from time import time
from socket import socket


for n in range(100):
    t=time()
    s=socket()
    s.connect(('127.0.0.1',4321))
    print(n,time()-t)
