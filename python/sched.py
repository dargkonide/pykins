from threading import Thread
from queue import Queue
from time import time,sleep

import traceback

def scheduler(data):
    while 1:
        try:
            if data['host']==data['x']['master']:
                for n in data['x']['scheduler'].copy():
                    if time()>=n['start']:
                        print(n)
                        data['x']['scheduler'].remove(n)
                        master=data['x']['master']
                        data['send'].put((master,{'n':'run','v':n['name'],'vars':n['vars'],'r':n['id']},None))
        except:
            with open('err.log','a') as ff:
                traceback.print_exc()
                traceback.print_exc(file=ff)
        sleep(1)
qsend=Queue()

def work(data):
    Thread(target=scheduler,args=(data,)).start()
    q=Queue()
    data['subproxy']['schedule']=q
    while 1:
        try:
            con,x=q.get()
            if x['n']=='schedule':
                data['x']['schedule'].append(x['v'])
        except:
            with open('err.log','a') as ff:
                traceback.print_exc()
                traceback.print_exc(file=ff)