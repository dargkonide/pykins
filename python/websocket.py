from simple_websocket_server import WebSocketServer, WebSocket
from json import loads,dumps
from time import sleep
from dateutil import parser
from threading import Thread
from random import randint
import traceback

tiper={int:'string',str:'string',list:'select',tuple:'multiselect',bool:'checkbox'}
class SimpleEcho(WebSocket):

    def xsend(self,msg):
        self.send_message(msg)
        print(msg)

    def handle(self):
        try:


            msg=loads(self.data)
            print(msg)

            if msg.get('type')=="scheds":
                self.send_message(dumps(gdata['x']['scheduler']))
            if msg.get('type')=="schedule":
                print(msg)
                gdata['x']['scheduler'].append({'time':msg['time'],'name':msg['name'],'vars':msg['vars']})

            if msg.get('type')=="schedule_select":
                print(msg)
                job_vars={n['name']:n['value'] for n in msg['vars']}
                start=parser.parse(msg['start']).timestamp()
                end=parser.parse(msg['end']).timestamp()
                gdata['x']['scheduler'].append({'start':start,'end':end,'name':msg['name'],'vars':job_vars})
            if msg.get('type')=="getCode":
                job=gdata['x']['jobs'].get(msg['name'])
                self.xsend(dumps({'type':'getCode','code':job['code']}))
                # self.send_message
            if msg.get('type')=="getVars":
                job=gdata['x']['jobs'].get(msg['name'])
                print('Send', {'type':'getVars','code':job['vars']})
                self.send_message(dumps({'type':'getVars','vars':job['vars']}))
            if msg.get('type')=="setCode":
                job=gdata['x']['jobs'].get(msg['name'])
                job['code']=msg['code']
                xjob=job.copy()
                xjob['name']=msg['name']
                print('Send', {'type':'job','msg':xjob})
                [n.send_message(dumps({'type':'job','msg':xjob})) for n in clients if n is not self]
            if msg.get('type')=="setVars":
                job=gdata['x']['jobs'].get(msg['name'])
                job['vars']=msg['vars']
                xjob=job.copy()
                xjob['name']=msg['name']
                print('Send', {'type':'job','msg':xjob})
                [n.send_message(dumps({'type':'job','msg':xjob})) for n in clients if n is not self]
            if msg.get('type')=="jobs":
                jobs=[{'name':k,'status':v['status']} for k,v in gdata['x']['jobs'].items()]
                # print('Send', {'type':'jobs','msg':jobs})
                # print('=======================')
                # print(gdata['x'])
                # print('=======================')
                self.send_message(dumps({'type':'jobs','msg':jobs}))
            if msg.get('type')=="job":
                job=gdata['x']['jobs'].get(msg['msg']).copy()
                job['name']=msg['msg']
                print('Send', {'type':'job','msg':job})
                self.send_message(dumps({'type':'job','msg':job}))
            if msg.get('type')=="hosts":
                hosts={'master':gdata['x']['master'], 'servers':gdata['x']['servers']} 
                print('Send', {'type':'hosts','msg':hosts})
                self.send_message(dumps({'type':'hosts','msg':hosts}))
            if msg.get('type')=="name":
                job: dict=gdata['x']['jobs'].pop(msg['old'])
                print(f'Change job name from {msg["old"]} to {msg["new"]}')
                gdata['x']['jobs'][msg['new']]=job
            if msg.get('type')=="build":
                job=gdata['x']['jobs'].get(msg['name']).copy()
                job_vars=gdata['imports']['executor'].run(job['vars'],gdata,{},-1)
                job_vars.pop('run_id')
                job_vars=[{'name':k,'value':v,'type':tiper.get(type(v),'xzchto')} for k,v in job_vars.items()]
                self.send_message(dumps({'type':'build','msg':job_vars}))
        except:
            print(self.data)
            traceback.print_exc()

    def connected(self):
        print(self.address, 'connected')
        clients.append(self)
        # Thread(target=run,args=(self,)).start()
        

    def handle_close(self):
        print(self.address, 'closed')
        clients.remove(self)

clients=[]
gdata=None
def work(data):
    global gdata
    gdata=data
    server = WebSocketServer('0.0.0.0', 5123, SimpleEcho)
    server.serve_forever()

