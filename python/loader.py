import os
import traceback
from time import sleep
from queue import Queue,Empty
from json import loads,dumps

q=Queue()

def load():
    jobs={}
    for a,b,c in os.walk('jobs'):
        if not b:
            for n in c:
                if '.py' in n:
                    with open(os.path.join(a,n),encoding='utf-8') as f:
                        jobs.setdefault(a.split(os.sep)[1],{}).update({n.split('.')[0]:f.read()})
                if '.json' in n:
                    with open(os.path.join(a,n),encoding='utf-8') as f:
                        jobs.setdefault(a.split(os.sep)[1],{}).update({n.split('.')[0]:loads(f.read())})
    return jobs

def dump(data):
    for n,p in data['x']['jobs'].items():
        job_dir=os.path.join('jobs',n)
        if not os.path.isdir(job_dir):
            os.mkdir(job_dir)
        for k,v in p.items():
            item=os.path.join(job_dir,k)
            with open(item+'.py' if type(v)==str else item+'.json','w',encoding='utf-8') as f:
                f.write(v if type(v)==str else dumps(v))

def dump_logs(data):
    for n,v in data['logs'].items():
        log_path=os.path.join('logs',n)+'.log'
        with open(log_path,'w',encoding='utf-8') as f:
            f.write('\n'.join(v))

def load_logs(data):
    for a,b,c in os.walk('logs'):
        for n in c:
            with open(os.path.join(a,n),encoding='utf-8') as f:
                data['logs'][n[:-4]]=[f.read()]
        

def work(data):
    data['x']['jobs']=load()
    load_logs(data)
    while 1:
        try:
            q.get()
            dump(data)
            dump_logs(data)
        except:
            with open('err.log','a') as ff:
                traceback.print_exc()
                traceback.print_exc(file=ff)

if __name__ == '__main__':
    data={'logs':{}}
    load_logs(data)
 
    print(data)