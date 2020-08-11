from queue import Queue
from json import dumps

import traceback

qsend={}

def work(data):
    q=Queue()
    data['subproxy'].append(q)
    while 1:
        try:
            con,x=q.get()
            if x['n']=='logs':
                data['logs'].setdefault(x['i']+x['j'],[]).append(x['v'])
                for n in qsend.get(x['i']+x['j'],[]):
                    n.send_message(dumps({'type':'glu','logs':x['v']}))

                # print(f"{x['j']} #{x['i']}: {x['v']}")
        except:
            with open('err.log','a') as ff:
                traceback.print_exc()
                traceback.print_exc(file=ff)