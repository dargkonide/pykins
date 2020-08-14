from socket import gethostname
from pickle import dumps,loads

from time import time
import traceback

def send(con,x):
    con.send(dumps(x)+b'<~>')

def read(con):
    buf=b''
    while buf[-3:]!=b'<~>':
        try:data=con.recv(4096)
        except:break
        if data:buf+=data
        else:break
    return [loads(n) for n in buf.split(b'<~>') if n]

