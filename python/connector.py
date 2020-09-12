from socket import socket,AF_INET,SOCK_STREAM,gethostbyname,gethostname,SOL_SOCKET,SO_REUSEADDR
from threading import Thread,Lock
from time import sleep

from exe.proto import *

import traceback


xlock=Lock()
s=socket(AF_INET,SOCK_STREAM)
s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
s.bind(('',5132))
s.listen(10)

def acceptor(data):
    while 1:
        try:
            con,addr=s.accept()
            ips=data['x']['ip']
            if ips.get(addr[0]):  
                host=read(con)[0]
                data['connects'].setdefault(addr[0],[]).append(con)
                print(f'{host} s connected')
            else:
                host=read(con)[0]
                data['x']['servers'].append(host)
                data['x']['ip'][addr[0]]=host
                data['x']['host'][host.split('.')[0]]=addr[0]
                data['connects'].setdefault(addr[0],[]).append(con)
                print(f'New host {host} connected',)
                if data['host']==data['x']['master']:
                    for n in ips:
                        if data['connects'].get(n):
                            data['send'].put((data['x']['ip'][n].split('.')[0],{'n':'new','v':data['x']}))
                            
                

        except:
            with open('err.log','a') as ff:
                traceback.print_exc()
                traceback.print_exc(file=ff)

        


def work(data):
    Thread(target=acceptor,args=(data,)).start()
    while 1:
        try:
            ips=data['x']['ip'].copy()
            for n in ips:
                if not data['connects'].get(n):
                    try:
                        s=socket(AF_INET,SOCK_STREAM)
                        s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
                        s.connect((n,5132))
                        send(s,data['host'])
                        data['connects'].setdefault(n,[]).append(s)
                        print(f'{ips[n].split(".")[0]} c connected')
                    except:
                        with open('err.log','a') as ff:
                            ff.write(f'Can\'t connect {n}\n')
        except:
            with open('err.log','a') as ff:
                traceback.print_exc(file=ff)
                ff.write(str(data))
        sleep(0.05)

if __name__=="__main__":
    acceptor()