from threading import Thread
from socket import gethostname
from time import sleep

from exe.proto import *

lisn=set()


def lisner(ip,con,data):
    host=data['x']['ip'].get(ip).split('.')[0]
    print(f'lisn: {host}')
    while 1:
        try:
            for x in read(con):
                # print(x)
                if x['n']=='new':
                    data['x']=x['v']
                if x['n']=='get':
                    send(con,{'n':'new','v':data['x']})
                if x['n']=='ping':
                    send(con,{'n':'pong'})
                if data['subscribe'].get(host):
                    for n in data['subscribe'][host]:
                        n.put(x)
                for n in data['subproxy']:
                    n.put((host,x))
        except:
            traceback.print_exc()
            data['connects'][ip].remove(con)
            if not data['connects'][ip]:
                data['connects'].pop(ip)
                lisn.discard(con)
                print(f'{host} disconnected')
            with open('err.log','a') as ff:
                traceback.print_exc(file=ff)
            break

def work(data):
    while 1:
        try:
            if data.get('connects'):
                for n in list(data['connects'].keys()):
                    if data['x']['ip'].get(n)!=data['host'] and data['host']==data['x']['master']:
                        data['send'].put((data['x']['ip'].get(n),{'n':'new','v':data['x']}))
                    for con in set(data['connects'][n])-lisn:
                        Thread(target=lisner,args=(n,con,data)).start()
                        lisn.add(con)
        except:
            with open('err.log','a') as ff:
                traceback.print_exc()
                traceback.print_exc(file=ff)
        sleep(0.05)