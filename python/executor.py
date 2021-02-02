from multiprocessing import Queue as PQueue
from multiprocessing import Process
from threading import Thread,Lock
from datetime import datetime
from requests import get
from queue import Queue,Empty
from time import sleep

import os
import process
from exe.proto import *

def waiter(pdata,data,pin):
    host,msg=pdata
    sended=Queue()
    while 1:
        data['send'].put((host,msg,sended))
        if not sended.get():
            master=data['x']['master']
            data['send'].put((master,{'n':'logs','v':f"Node {host} is offline, waiting ...",'i':msg['r'],'j':msg['j']},None))
            sleep(15)
        else:break
    ret=Queue()
    data['subscribe'].setdefault(host,[]).append(ret)
    while 1:
        x=ret.get()
        if x.get('n')=="executed" :#and x.get('r')==run_id and x.get('j')==job_name:
            break
    data['subscribe'][host].remove(ret)
    pin.put(x['v'])

def waiter_result(qout,pin):
    pin.put(qout.get())

def connector(pin,pout,data,p):
    while p.is_alive():
        try:
            type_data,pdata=pout.get(timeout=10)
            if type_data=='node':
                Thread(target=waiter,args=(pdata,data,pin)).start()
            if type_data=='log':
                master=data['x']['master']
                data['send'].put((master,pdata,None))
            if type_data=='run_job':
                name,job_vars,wait,run_id,job_name=pdata
                new_run_id=str(data['x']['jobs'][name]['last_build_id'])
                data['x']['jobs'][name]['last_build_id']+=1
                conf={'n':'run','v':name,'r':new_run_id,'vars':job_vars}
                if wait:
                    qout=Queue()
                    conf['q']=qout
                q.put((None,conf))
                master=data['x']['master']
                log_msg=f"Building #{new_run_id} {name}: http://{master}:8000/jobs/{name}/history/{new_run_id}/logs"
                data['send'].put((master,{'n':'logs','v':log_msg,'i':run_id,'j':job_name},None))
                if wait:
                    Thread(target=waiter_result,args=(qout,pin)).start()
                
        except Empty:
            pass
        except:
            traceback.print_exc()

def open_process(data):
    qin,quot,pin,pout=PQueue(),PQueue(),PQueue(),PQueue()
    p=Process(target=process.process,args=(qin,quot,pin,pout))
    p.start()
    Thread(target=connector,args=(pin,pout,data,p)).start()
    pool.put((qin,quot,pin,pout,p))

q=Queue()
qhistory={}

pool=Queue()
lock=Lock()

def send_history(data,x):
    history=[{
    'id':k,
    'status':v['status'],
    'start':v.get('start',''),
    'end':v.get('end',''),
    'delta':v.get('delta','')} for k,v in data['x']['jobs'][x['v']]['history'].items()]
    for n in qhistory.get(x['v'],[]):
        n.xsend({'type':'history','msg':history})

def set_workspace(job_name):
    i=1
    workspase=f'workspace/{job_name}'
    while 1:
        if not os.path.isdir(workspase):
            os.mkdir(workspase)
        if '__lock__' in os.listdir(workspase):
            i+=1
            workspase=f'workspace/{job_name}_{i}'
        else:
            open(f'{workspase}/__lock__','w').close()
            break
    return workspase

def get_vault(path):
    try:
        r=get(f'http://tkli-erib0124.vm.mos.cloud.sbrf.ru:8200/v1/cubbyhole/{path}',
            headers={'X-Vault-Token':"s.hY3a8RZ3Wu6r8MeZPsSHmM2O"})
        return r.json().get('data',{})
    except:
        return {}

def work(data):
    with lock:
        if pool.empty():
            for n in range(10):
                open_process(data)

    if not 'exec' in data['subproxy']:
        data['subproxy']['exec']=q
        data['subproxy']['run']=q
    while 1:
        try:

            host,x=q.get()

            if host and x['n']=='exec':
                data['send'].put((data['x']['master'],{'n':'node_reg','r':x['r'],'j':x['j']},None))
                qin,quot,pin,pout,p=pool.get()
                data['running'].setdefault(f"{x['j']}_{x['r']}",[]).append(p)
                with lock:
                    workspace=set_workspace(x['j'])
                qin.put((x.get('c'),x['v'],x['r'],x['j'],workspace))
                result_vars=quot.get()
                try:data['running'][f"{x['j']}_{x['r']}"].remove(p)
                except:pass
                if p.is_alive():
                    pool.put((qin,quot,pin,pout,p))
                data['send'].put((host,{'n':'executed','v':result_vars,'r':x['r'],'j':x['j']},None))

            if x['n']=='run':
                print('run')
                if x.get('r'):run_id=x['r']
                else:
                    run_id=str(data['x']['jobs'][x['v']]['last_build_id'])
                    data['x']['jobs'][x['v']]['last_build_id']+=1
                data['x']['jobs'][x['v']]['history'][run_id]={}
                data['x']['jobs'][x['v']]['history'][run_id]['vars']=x['vars']
                data['x']['jobs'][x['v']]['history'][run_id]['status']='sheduled'
                send_history(data,x)
                # v=run(data['x']['jobs'][x['v']]['code'],data,x['vars'],run_id,x['v'])
                qin,quot,pin,pout,p=pool.get()
                data['running'].setdefault(f"{x['v']}_{run_id}",[]).append(p)
                data['x']['jobs'][x['v']]['history'][run_id]['status']='running'
                data['x']['jobs'][x['v']]['history'][run_id]['nodes']=[data['x']['master']]
                send_history(data,x)
                start_time=datetime.now()
                data['x']['jobs'][x['v']]['history'][run_id]['start']=str(start_time).split('.')[0]
                with lock:
                    workspace=set_workspace(x['v'])

                job_vars=x['vars'].copy()
                job_vars.update(get_vault(x['v']))

                qin.put((data['x']['jobs'][x['v']]['code'],job_vars,run_id,x['v'],workspace))
                result_vars=None
                while p.is_alive():
                    try:
                        result_vars=quot.get(timeout=1)
                        break
                    except:pass
                data['running'].pop(f"{x['v']}_{run_id}")
                if p.is_alive():
                    pool.put((qin,quot,pin,pout,p))
                end_time=datetime.now()
                data['x']['jobs'][x['v']]['history'][run_id]['end']=str(end_time).split('.')[0]
                data['x']['jobs'][x['v']]['history'][run_id]['delta']=str(end_time-start_time).split('.')[0]

                if not result_vars:
                    status='stopped'
                elif result_vars.get('trace'):
                    status='failed'  
                else:
                    status='success'
                data['x']['jobs'][x['v']]['history'][run_id]['status']=status
                data['x']['jobs'][x['v']]['status']=[status]
                send_history(data,x)
                if x.get('q'):x['q'].put((status,result_vars))
                # print(job['history'])
                # print(data['x']['jobs'][x['v']]['history'])
        except:
            with open('err.log','a') as ff:
                traceback.print_exc()
                traceback.print_exc(file=ff)

# patch(open('exe/test.py',encoding='utf-8').read())