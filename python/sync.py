from threading import Thread
from socket import gethostname
from time import sleep,time

from exe.proto import *
import socket
lisn=set()

def lisner(ip,con,data):
    host=data['x']['ip'].get(ip).split('.')[0]
    # print(f'lisn: {host}')
    while 1:
        try:
            recv=read(con)
            if not recv:break
            for x in recv:
                if x['n']=='get_host':
                    data['send'].put((host,{'n':'host','v':data['host']},None))
                if x['n']=='new':
                    print('new')
                    data['x']=x['v']
                if x['n']=='get':
                    send(con,{'n':'new','v':data['x']})
                if x['n']=='ping':
                    data['send'].put((host,{'n':'pong'},None))
                    data['ping'][host]=time()
                if x['n']=='pong':
                    data['ping'][host]=time()
                if x['n']=='kill':
                    print(f"kill {x['j']} #{x['r']}")
                    for p in data['running'][f"{x['j']}_{x['r']}"]:
                        print(p,p.is_alive())
                        if p.is_alive():
                            p.terminate()
                            data['imports']['executor'].open_process(data)

                if x['n']=='node_reg':
                    data['x']['jobs'][x['j']]['history'][x['r']]['nodes'].append(host)
                if data['subscribe'].get(host):
                    for n in data['subscribe'][host]:
                        n.put(x)
                if data['subproxy'].get(x['n']):
                    data['subproxy'][x['n']].put((host,x))
        except:
            traceback.print_exc()
            break
        finally:
            con.close()

def get_host_send(addr):
    rcon=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    rcon.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        rcon.connect((addr[0],5132))
        with rcon:
            send(rcon,{'n':'get_host'})
    except:
        pass



s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('',5132))
s.listen(1000)
def work(data):
    while 1:
        try:
            con,addr=s.accept()
            ips=data['x']['ip']
            if not ips.get(addr[0]):
                print(addr)
                msg=read(con)[0]
                if msg.get('n')=='host':
                    host=msg['v'] 
                    data['x']['servers'].append(host)
                    data['x']['ip'][addr[0]]=host
                    data['x']['host'][host.split('.')[0]]=addr[0]
                    print(f'New host {host} connected')
                    for server in data['x']['servers']:
                        if not data['host'] in server:
                            data['send'].put((server,{'n':'new','v':data['x']},None))
                else:
                    Thread(target=get_host_send,args=(addr,)).start()
                    continue
            if ips.get(addr[0]):
                Thread(target=lisner,args=(addr[0],con,data)).start()

            # if data.get('connects'):
            #     for n in list(data['connects'].keys()):
            #         if data['x']['ip'].get(n)!=data['host'] and data['host']==data['x']['master']:
            #             data['send'].put((data['x']['ip'].get(n),{'n':'new','v':data['x']}))
            #         for con in set(data['connects'][n])-lisn:
            #             Thread(target=lisner,args=(n,con,data)).start()
            #             lisn.add(con)
        except:
            with open('err.log','a') as ff:
                traceback.print_exc()
                traceback.print_exc(file=ff)
        # sleep(0.05)