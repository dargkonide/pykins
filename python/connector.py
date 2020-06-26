from socket import socket,AF_INET,SOCK_STREAM,gethostbyname,gethostname
from threading import Thread,Lock
from time import sleep
import traceback


xlock=Lock()
s=socket(AF_INET,SOCK_STREAM)
s.bind(('',5032))
s.listen(10)

def acceptor(data):
    while 1:
        try:
            con,addr=s.accept()
            ips=data['x']['ip']
            if ips.get(addr[0]):  
                data['connects'].setdefault(addr[0],[]).append(con)
                print(f'{ips[addr[0]].split(".")[0]} s connected')
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
                        s.connect((n,5032))
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