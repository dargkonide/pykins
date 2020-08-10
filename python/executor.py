from importlib import util
from queue import Queue
from uuid import uuid4
from time import time,sleep
from re import search,findall
from os import popen,remove

import os
import shutil

from exe.proto import *

   
def patch(code):
    test_tabs=[]
    for n in code.split('\n'):
        v=search(r'^\s*',n)[0]
        if len(v):
            t=v[0]
            test_tabs.append(len(v))
    if test_tabs:j=min(test_tabs)
    else:t=' ';j=4

    patch_code=''
    min_len=None
    for n in code.split('\n'):
        if min_len is not None:
            t_k=len(search(r'^\s*',n)[0])
            if t_k>min_len or not n.strip():
                patch_code+=n[min_len+j:]+'\n'
                continue
            else:
                patch_code=patch_code[:-1]
                patch_code+="''')\n"
                min_len=None
        else:
            if 'with node' in n and not search(r'^\s*#',n):
                k=search(r'^\s*',n)[0]
                node=findall(r"(node\(.*)\)",n)
                min_len=len(k)
                patch_code+=k+f"{node[0]},vars(),data,run_id,job_name,'''\n"
                continue
        n=n.replace('print(','print(data,run_id,job_name,')
        patch_code+=n+'\n'
    if min_len is not None:
        patch_code=patch_code[:-1]
        patch_code+="''')\n"
    return patch_code

def ufilt(d):
    newd={}
    for k,v in d.items():
        if k in ['addr','module','data']:
            continue
        if '__' in k:
            continue
        if not type(v) in [str,dict,list,tuple,int,set,bool]:
            continue
        newd[k]=v
    # print(newd)
    return newd

def println(data,run_id,job_name,*args,**kwargs):
    # print(*args,**kwargs)
    master=data['x']['master']
    ip_master=data['x']['host'].get(master)
    z=data['connects'].get(ip_master)
    data['send'].put((master,{'n':'logs','v':str(' '.join(str(n) for n in args)),'i':run_id,'j':job_name}))

def node(host,vrs,data,run_id,job_name,code):
    data['send'].put((host,{'n':'exec','c':code,'v':ufilt(vrs),'r':run_id,'j':job_name}))
    ret=Queue()
    data['subscribe'].setdefault(host,[]).append(ret)
    while 1:
        x=ret.get()
        if x.get('n')=="executed" :#and x.get('r')==run_id and x.get('j')==job_name:
            # print(x)
            vrs.update(x['v'])
            break
    data['subscribe'][host].remove(ret)

def run(code,data,vrs,run_id,job_name):
    # print(f'run: #{run_id} {job_name} {code} ')
    module=str(uuid4())
    path=f'exe/{module}.py'
    with open(path,'w',encoding='utf-8') as f:
        f.write(patch(code))
    spec=util.spec_from_file_location(module,f"exe/{module}.py")
    x=util.module_from_spec(spec)
    vars(x).update(vrs)
    vars(x).update({'data':data,'run_id':run_id,'node':node,'send':send,'print':println,'job_name':job_name})
    target_dir=os.path.abspath(os.getcwd())
    try:
        spec.loader.exec_module(x)
    except:
        trace=traceback.format_exc()
        vars(x).update({'trace':trace})
        master=data['x']['master']
        data['send'].put((master,{'n':'logs','i':run_id,'j':job_name,'v':trace}))
    os.chdir(target_dir)
    result=ufilt(vars(x))
    del x
    remove(path)
    shutil.rmtree('exe/__pycache__', ignore_errors=True)
    return result

q=Queue()

def work(data):
    if not q in data['subproxy']:
        data['subproxy'].append(q)
    while 1:
        try:
            host,x=q.get()
            if host and x['n']=='exec':
                v=run(x.get('c'),data,x['v'],x['r'],x['j'])
                data['send'].put((host,{'n':'executed','v':v,'r':x['r'],'j':x['j']}))
            if x['n']=='run':
                job=data['x']['jobs'][x['v']]
                history=job['history']
                if x.get('r'):
                    run_id=x['r']
                else:
                    run_id=str(job['last_build_id'])
                    job['last_build_id']+=1
                history[run_id]={}
                history[run_id]['status']='running'
                v=run(job['code'],data,x['vars'],run_id,x['v'])
                history[run_id]['status']='failed' if v.get('trace') else 'success'
        except:
            with open('err.log','a') as ff:
                traceback.print_exc()
                traceback.print_exc(file=ff)

# patch(open('exe/test.py',encoding='utf-8').read())