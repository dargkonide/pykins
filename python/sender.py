from threading import Thread
from exe.proto import *
from queue import Queue
from time import sleep
import traceback

def sleeper(data,qoutput,wait=10):
    sleep(wait)
    qoutput.put(data)

def work(data):
    while 1:
        try:
            host,msg=data['send'].get()
            ip=data['x']['host'].get(host.split('.')[0])
            z=data['connects'].get(ip)
            if not z:
                print(f"Node {host} is offline, waiting ...")
                Thread(target=sleeper,args=((host,msg),data['send'])).start()
                continue
            # print(f'send: {msg}')
            send(z[0],msg)
        except:
            with open('err.log','a') as ff:
                traceback.print_exc()
                traceback.print_exc(file=ff)