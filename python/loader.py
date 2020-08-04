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
                    with open(os.path.join(a,n)) as f:
                        jobs.setdefault(a.split(os.sep)[1],{}).update({n.split('.')[0]:f.read()})
                if '.json' in n:
                    with open(os.path.join(a,n)) as f:
                        jobs.setdefault(a.split(os.sep)[1],{}).update({n.split('.')[0]:loads(f.read())})
    return jobs

def dump(data):
    for n,p in data['x']['jobs'].items():
        job_dir=os.path.join('jobs',n)
        if not os.path.isdir(job_dir):
            os.mkdir(job_dir)
        for k,v in p.items():
            item=os.path.join(job_dir,k)
            with open(item+'.py' if type(v)==str else item+'.json','w') as f:
                f.write(v if type(v)==str else dumps(v))

def work(data):
    data['x']['jobs']=load()
    while 1:
        try:
            q.get()
            dump(data)
        except:
            with open('err.log','a') as ff:
                traceback.print_exc()
                traceback.print_exc(file=ff)

if __name__ == '__main__':
    jobs=load()
    jobs['new']=jobs['start_scenario']
    dump(jobs)
    print(jobs)