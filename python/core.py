from importlib import import_module
from threading import Thread
from os.path import dirname
from socket import gethostbyname
from queue import Queue
from os import listdir


imports={}
data={'send':Queue(),'imports':imports,'connects':{},'subscribe':{},'subproxy':[],'x':{
'servers':['95.24.211.79'],
'master':'DESKTOP-50TJ75T',
'jobs':{
    'test':{
        'vars':{},
        'code':'print(1)',
        'status':True,
        'history':[]
    }
},
'scheduler':[]
}}

data['x']['ip']={gethostbyname(n):n for n in data['x']['servers']}
data['x']['host']={n.split('.')[0]:gethostbyname(n) for n in data['x']['servers']}
threads=[]
tcount={}


for n in listdir(dirname(__file__)):
    if n[-3:]=='.py' and n[:-3]!='core' and not imports.get(n[:-3]):
        n=n[:-3]
        print(n)
        imports[n]=import_module(n)
        
        for m in range(tcount.get(n,1)):
            threads.append(Thread(target=imports[n].work,args=(data,)))

for n in threads:n.start()
for n in threads:n.join()
