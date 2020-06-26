from importlib import util
from queue import Queue
from uuid import uuid4
from time import time,sleep
from re import search,findall
from os import popen,remove

import os

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
                patch_code+=k+f"{node[0]},vars(),data,'''\n"
                continue
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

def println(*args,**kwargs):
    # print(*args,**kwargs)
    master=gdata['x']['master']
    ip_master=gdata['x']['host'].get(master)
    z=gdata['connects'].get(ip_master)
    gdata['send'].put((master,{'n':'logs','v':args}))

def node(host,vrs,data,code):
    data['send'].put((host,{'n':'exec','c':code,'v':ufilt(vrs)}))
    ret=Queue()
    data['subscribe'][host]=ret
    while 1:
        x=ret.get()
        if x.get('n')=="executed":
            vrs.update(x['v'])
            break

def run(code,data,vrs):
    module=str(uuid4())
    path=f'exe/{module}.py'
    with open(path,'w',encoding='utf-8') as f:
        f.write(patch(code))
    spec=util.spec_from_file_location(module,f"exe/{module}.py")
    x=util.module_from_spec(spec)
    vars(x).update(vrs)
    vars(x).update({'data':data,'node':node,'send':send,'print':println})
    target_dir=os.path.abspath(os.getcwd())
    try:
        spec.loader.exec_module(x)
    except:
        trace=traceback.format_exc()
        master=gdata['x']['master']
        data['send'].put((master,{'n':'logs','v':(trace,)}))
    os.chdir(target_dir)
    result=ufilt(vars(x))
    del x
    remove(path)
    remove(f'exe/__pycache__/{module}.cpython-38.pyc')
    return result

def work(data):
    global gdata
    gdata=data
    if gethostname() in data['x']['master']:
        sleep(0.05)
        t=time()
        run(open('exe/test.py',encoding='utf-8').read(),data,{})
        print(time()-t)
    q=Queue()
    data['subproxy'].append(q)
    while 1:
        try:
            host,x=q.get()
            if x['n']=='exec':
                v=run(x.get('c'),data,x['v'])
                data['send'].put((host,{'n':'executed','v':v}))
        except:
            with open('err.log','a') as ff:
                traceback.print_exc()
                traceback.print_exc(file=ff)

# patch(open('exe/test.py',encoding='utf-8').read())