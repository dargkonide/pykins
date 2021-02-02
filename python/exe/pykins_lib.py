def ufilt(d):
    from pickle import dumps
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

def node(host,vrs,data,run_id,job_name,code):
    pin,pout=data
    # print(ufilt(vrs))
    pout.put(('node',(host,{'n':'exec','c':code,'v':ufilt(vrs),'r':run_id,'j':job_name})))
    vrs.update(pin.get())

def shell(cmd):
    from subprocess import Popen,PIPE
    from uuid import uuid4
    import os
    import platform
    bat_file=f'{uuid4()}.bat'
    with open(bat_file,'w') as f:
        f.write(cmd)
    try:
        cmd=['sh',bat_file]
        if platform.system()=='Windows':
            cmd=bat_file
        with Popen(cmd, stdout=PIPE) as p:
            while p.returncode is None:
                line=p.stdout.readline()
                if line:
                    if platform.system()=='Windows':
                        print(line.decode('cp1251').strip())
                    else:
                        print(line.decode('utf-8').strip())
                else:break
    finally:
        os.remove(bat_file)

def run_job(name,job_vars={},wait=True):
    pin,pout=data
    pout.put(('run_job',(name,job_vars,wait,run_id,job_name)))
    if wait:
        return pin.get()