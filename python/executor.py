from multiprocessing import Queue as PQueue
from multiprocessing import Process
from queue import Queue
from threading import Thread,Lock
from datetime import datetime

import process
from exe.proto import *

def waiter(pdata,data,pin):
    host,msg=pdata
    data['send'].put((host,msg))
    ret=Queue()
    data['subscribe'].setdefault(host,[]).append(ret)
    while 1:
        x=ret.get()
        if x.get('n')=="executed" :#and x.get('r')==run_id and x.get('j')==job_name:
            break
    data['subscribe'][host].remove(ret)
    pin.put(x['v'])

def connector(pin,pout,data,p):
    while p.is_alive():
        try:
            type_data,pdata=pout.get(timeout=10)
            if type_data=='node':
                Thread(target=waiter,args=(pdata,data,pin)).start()
            if type_data=='log':
                master=data['x']['master']
                data['send'].put((master,pdata))
        except:
            pass
        

q=Queue()
qhistory={}

pool=Queue()
lock=Lock()

def send_history(data,x):
    history=[{'id':k,'status':v['status'],'start':v.get('start',''),'end':v.get('end',''),'delta':v.get('delta','')} for k,v in data['x']['jobs'][x['v']]['history'].items()]
    for n in qhistory.get(x['v'],[]):
        n.xsend({'type':'history','msg':history})

def work(data):
    with lock:
        if pool.empty():
            for n in range(10):
                qin,quot,pin,pout=PQueue(),PQueue(),PQueue(),PQueue()
                p=Process(target=process.process,args=(qin,quot,pin,pout))
                p.start()
                Thread(target=connector,args=(pin,pout,data,p)).start()
                pool.put((qin,quot,pin,pout,p))

    if not q in data['subproxy']:
        data['subproxy'].append(q)
    while 1:
        try:
            host,x=q.get()
            if host and x['n']=='exec':
                qin,quot,pin,pout,p=pool.get()
                qin.put((x.get('c'),x['v'],x['r'],x['j']))
                v=quot.get()
                pool.put((qin,quot,pin,pout,p))
                data['send'].put((host,{'n':'executed','v':v,'r':x['r'],'j':x['j']}))
            if x['n']=='run':
                if x.get('r'):run_id=x['r']
                else:
                    run_id=str(data['x']['jobs'][x['v']]['last_build_id'])
                    data['x']['jobs'][x['v']]['last_build_id']+=1
                data['x']['jobs'][x['v']]['history'][run_id]={}
                data['x']['jobs'][x['v']]['history'][run_id]['status']='sheduled'
                send_history(data,x)
                # v=run(data['x']['jobs'][x['v']]['code'],data,x['vars'],run_id,x['v'])
                qin,quot,pin,pout,p=pool.get()
                data['x']['jobs'][x['v']]['history'][run_id]['status']='running'
                send_history(data,x)
                start_time=datetime.now()
                data['x']['jobs'][x['v']]['history'][run_id]['start']=str(start_time).split('.')[0]
                qin.put((data['x']['jobs'][x['v']]['code'],x['vars'],run_id,x['v']))
                v=quot.get()
                pool.put((qin,quot,pin,pout,p))
                end_time=datetime.now()
                data['x']['jobs'][x['v']]['history'][run_id]['end']=str(end_time).split('.')[0]
                data['x']['jobs'][x['v']]['history'][run_id]['delta']=str(end_time-start_time).split('.')[0]
                data['x']['jobs'][x['v']]['history'][run_id]['status']='failed' if v.get('trace') else 'success'
                data['x']['jobs'][x['v']]['status']=['failed' if v.get('trace') else 'success']
                send_history(data,x)
                # print(job['history'])
                # print(data['x']['jobs'][x['v']]['history'])
        except:
            with open('err.log','a') as ff:
                traceback.print_exc()
                traceback.print_exc(file=ff)

# patch(open('exe/test.py',encoding='utf-8').read())