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
        'servers':['DESKTOP-50TJ75T', 'ilya_pc'],
        'master':'DESKTOP-50TJ75T',
        'jobs':{
            'start_scenario':{
                'vars':"""stend='NT1'
group='NT1'
scenario_id='252'
branchLTScripts='master'
branchDatapools='master'
scheduler='L'
profile_percentage='100'
target_comment='НТ1 надежность'
test_time=True
influx_drop=True
skip_pending=True
disable_transactions=True
M_TEST=''
jira_comment=''
user='khudyakov1-ad'
wait_shd=False
properties_scheduler=''""",
                'code':open('exe/start_scenario.py',encoding='utf-8').read(),
                'history':[],
                'status':1
            }
        },
        'scheduler':[]
    },
    'history':{}
}
# if data['host']==data['x']['master']:
#     data['x']['scheduler'].append({'time':time(),'name':'start_scenario',
#         'vars':data['x']['jobs']['start_scenario']['vars']})

data['x']['ip']={gethostbyname(n):n for n in data['x']['servers']}
data['x']['host']={n.split('.')[0]:gethostbyname(n) for n in data['x']['servers']}
threads=[]
tcount={}

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
