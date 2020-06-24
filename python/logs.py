from queue import Queue

import traceback

qsend=Queue()

def work(data):
    q=Queue()
    data['subproxy'].append(q)
    while 1:
        try:
            con,x=q.get()
            if x['n']=='logs':
                print(*x['v'])
        except:
            with open('err.log','a') as ff:
                traceback.print_exc()
                traceback.print_exc(file=ff)