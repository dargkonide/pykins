from importlib import import_module
from threading import Thread
from os.path import dirname
from socket import gethostname,gethostbyname
from queue import Queue
from time import time
from os import listdir

# TODO: 'servers':['artem_pc', 'ilya_pc'], 'master':'artem_pc' - add property and change this overlap setup
imports={}
data={'host':gethostname(),'send':Queue(),'imports':imports,'connects':{},'subscribe':{},'subproxy':[],'x':{
        'servers':[gethostname()],
        'master':gethostname(),
        'jobs':{},
        'scheduler':[]
    }
}
# if data['host']==data['x']['master']:
#     data['x']['scheduler'].append({'time':time(),'name':'start_scenario',
#         'vars':data['x']['jobs']['start_scenario']['vars']})

data['x']['ip']={gethostbyname(n):n for n in data['x']['servers']}
data['x']['host']={n.split('.')[0]:gethostbyname(n) for n in data['x']['servers']}
threads=[]
tcount={'executor':100}

filtr=['simple_websocket_server','core']

for n in listdir(dirname(__file__)):
    if n[-3:]=='.py' and not n[:-3] in filtr and not imports.get(n[:-3]):
        n=n[:-3]
        print(n)
        imports[n]=import_module(n)
        
        for m in range(tcount.get(n,1)):
            threads.append(Thread(target=imports[n].work,args=(data,)))

for n in threads:n.start()
for n in threads:n.join()
