from importlib import import_module
from threading import Thread
from os.path import dirname
from socket import gethostname,gethostbyname,getfqdn
from queue import Queue
from time import time
from os import listdir
 
import os

target_path=os.path.abspath(dirname(__file__))
os.chdir(target_path)

imports={}
data={'host':gethostname(),'running':{},'ping':{},'send':Queue(),'imports':imports,'connects':{},'subscribe':{},'subproxy':{},'x':{
        'servers':list({'cpython.site',getfqdn()}),
        'master':'tvsi-erib0054',
        'jobs':{},
        'scheduler':[]
    },'logs':{}
}

if __name__ == '__main__':
    data['send'].put((data['x']['master'],{'n':'host','v':data['host']},None))
    data['x']['ip']={gethostbyname(n):n for n in data['x']['servers']}
    data['x']['host']={n.split('.')[0]:gethostbyname(n) for n in data['x']['servers']}
    threads=[]
    tcount={'executor':100,'sender':100}
    filtr=['simple_websocket_server','core','process','ast']
    for n in listdir(target_path):
        if n[-3:]=='.py' and not n[:-3] in filtr and not imports.get(n[:-3]):
            n=n[:-3]
            print(n)
            imports[n]=import_module(n)
            
            for m in range(tcount.get(n,1)):
                threads.append(Thread(target=imports[n].work,args=(data,)))

    for n in threads:n.start()
    for n in threads:n.join()
