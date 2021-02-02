from threading import Thread
from exe.proto import *
from queue import Queue
from time import sleep
import traceback
import socket

# def sleeper(data,qoutput,wait=10):
#     sleep(wait)
#     qoutput.put(data)

def work(data):
    while 1:
        try:
            host,msg,error=data['send'].get()
            ip=data['x']['host'].get(host.split('.')[0])
            s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                s.connect((ip,5132))
            except:
                if error:error.put(False)
                continue
            
                
            # print(f'send: {msg}')
            with s:
                send(s,msg)
                if error:error.put(True)
        except:
            with open('err.log','a') as ff:
                traceback.print_exc()
                traceback.print_exc(file=ff)
        finally:
            try:del host,msg,error,s,ip
            except:pass