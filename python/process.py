from importlib import util
from exe.proto import *
from datetime import datetime
from queue import Queue
from time import time,sleep
from uuid import uuid4
from re import search,findall
from os import popen,remove

import shutil
import ast
import sys
import re
import os

with open('exe/pykins_lib.py',encoding='utf-8') as f:
    pykins_lib=f.read()+'\n'

def get_var_name():
    x=str(uuid4())
    if x[0].isdigit():
        x='x'+x[1:]
    return x.replace('-','_')

def patch(code_string):
    code_split=code_string.split('\n')
    code_ast = ast.parse(code_string)#Parse code and find "with" constructions
    with_nodes = [node for node in ast.walk(code_ast) if isinstance(node, ast.With)]

    filtr=[]
    nodes={}
    for with_node in with_nodes: 
        if re.match(r'.*with\s+node\s*\(',code_split[with_node.lineno-1]):#Проверяем что конструкция with содержит функцию node
            for i,node in enumerate(ast.walk(with_node)):
                if i and isinstance(node, ast.With):
                    filtr.append(node)#Фильтр для вложенных with node
            start=with_node.lineno-1
            if hasattr(with_node,'end_lineno'):#in python3.8
                end=with_node.end_lineno
            else:
                end=max(n.lineno for n in ast.walk(with_node) if hasattr(n,'lineno'))

            nodes[with_node]=(start,end,code_split[start:end])
    for n in filtr:#Фильтруем вложенные with node
        if nodes.get(n):nodes.pop(n)

    send_code_vars={}
    mapping=[]
    for k,v in nodes.items():
        start,end,code_list=v
        code='\n'.join(code_list)
        node=code.split(':')[0]
        index=node.index('with')
        if index>0:
            char=node[0]
            for i,n in enumerate(code_list):
                if n[:index]==char*index:
                    code_list[i]=n[index:]#Удаляем лишнюю табуляцию в конструкции with node
            code='\n'.join(code_list)
            node=code.split(':')[0]
        else:char=''

        send_code=[n for n in code[len(node)+1:].split('\n') if n.strip()]
        for i,n in enumerate(send_code):
            if not i:
                spaces=re.search(r'^\s*',n)[0]
            if spaces and n[:len(spaces)]==spaces:
                send_code[i]=n[len(spaces):]#Удаляем лишнюю табуляцию только в блоке кода конструкции with node
            send_code[i]
        code_var=get_var_name()
        node_vars=re.findall(r"(node\s*\(.*)\)",node.replace('\n',''))[0]
        node=f'{index*char}{node_vars},globals(),data,run_id,job_name,{code_var})'
        mapping.append((start,end,node))
        send_code_vars[code_var]='\n'.join(send_code)

    mapping.sort(key=lambda x:x[0])

    i=0
    new_code_split=[]
    while i<len(code_split):#Заменяем конструкции with node и собираем итоговый код
        continue_flag=False
        for start,end,node in mapping:
            if i in range(start,end):
                new_code_split.append(node)
                i=end
                continue_flag=True
                break
        if continue_flag:continue
        new_code_split.append(code_split[i])
        i+=1

    # for i,n in enumerate(new_code_split):
    #     new_code_split[i]=n.replace('print(','print(data,run_id,job_name,')

    new_code=pykins_lib+'\n'.join(new_code_split)
    
    return new_code,send_code_vars



def ufilt(d):
    newd={}
    for k,v in d.items():
        if k in ['addr','module','data']:
            continue
        if '__' in k:
            continue
        if not type(v) in [str,dict,list,tuple,int,float,set,bool,bytes]:
            continue
        try:dumps(v)
        except:continue
        newd[k]=v
    return newd



class output():
    buff=''
    def __init__(self,run_id,job_name,pout):
        self.run_id=run_id
        self.job_name=job_name
        self.pout=pout
    def write(self,msg):
        self.buff+=msg
        if '\n' in self.buff:
            for n in self.buff.split('\n'):
                if n.strip():
                    self.pout.put(('log',{'n':'logs','v':n,'i':self.run_id,'j':self.job_name}))
            self.buff=''

def run(code,data,vrs,run_id,job_name,workspace):
    if workspace:
        workspace=os.path.abspath(workspace)
        old_cwd=os.getcwd()
        os.chdir(workspace)
    pin,pout=data
    old_stdout,old_stderr=sys.stdout,sys.stderr
    new_stdout=output(run_id,job_name,pout)
    sys.stdout=new_stdout
    sys.stderr=new_stdout
    global_vars={}
    global_vars.update(vrs)
    global_vars.update({'data':data,'run_id':run_id,'job_name':job_name})
    code_vars={}
    try:
        code,code_vars=patch(code)
        global_vars.update(code_vars)
        exec(code,global_vars)
        
    except:
        trace=traceback.format_exc()
        global_vars.update({'trace':trace})
        traceback.print_exc()
    result=ufilt(global_vars)
    for n in list(code_vars.keys()&result.keys()):
        result.pop(n)
    sys.stdout,sys.stderr=old_stdout,old_stderr
    del new_stdout
    if workspace:
        os.chdir(workspace)
        os.remove('__lock__')
        os.chdir(old_cwd)
    return result


    

def process(qin,qout,pin,pout):
    while 1:
        try:
            code,vrs,run_id,job_name,workspace=qin.get()
            # print(f'run: #{run_id} {job_name} {code}')
            result=run(code,(pin,pout),vrs,run_id,job_name,workspace)
            qout.put(result)
        except:
            with open('err.log','a') as ff:
                traceback.print_exc()
                traceback.print_exc(file=ff)