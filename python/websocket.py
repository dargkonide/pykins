from simple_websocket_server import WebSocketServer, WebSocket
from json import loads,dumps
from time import sleep
from dateutil import parser
from threading import Thread
from random import randint
from datetime import datetime,timedelta
import traceback

iso=lambda x:datetime.fromtimestamp(x).isoformat()

tiper={int:'string',str:'string',list:'select',tuple:'multiselect',bool:'checkbox'}
class SimpleEcho(WebSocket):

    def xsend(self,msg):
        self.send_message(dumps(msg))
        print(f"Send: {msg}")

    def xsend_all(self,msg):
        for n in clients:
            n.send_message(dumps(msg))
        print(f"Send all: {msg}")

    def xsend_xall(self,msg):
        for n in clients:
            if self!=n:
                n.send_message(dumps(msg))
        print(f"Send xall: {msg}")

    def handle(self):
        try:


            msg=loads(self.data)
            print(f"Receive: {msg}")

            if msg.get('type')=="scheds":
                self.send_message(gdata['x']['scheduler'])
            if msg.get('type')=="schedule":
                print(msg)
                gdata['x']['scheduler'].append({'time':msg['time'],'name':msg['name'],'vars':msg['vars']})
            if msg.get('type')=="get_schedule":
                # n['date'] TODO: 
                events=[{'title':n['name'],'start':iso(n['start']),'end':iso(n['end'])} for n in gdata['x']['scheduler']]
                self.xsend({'type':'get_schedule','events':events})
            if msg.get('type')=="schedule_select":
                print(msg)
                job_vars={n['name']:n['value'] for n in msg['vars']}
                start=parser.parse(msg['start']).timestamp()
                end=parser.parse(msg['end']).timestamp()
                gdata['x']['scheduler'].append({'start':start,'end':end,'name':msg['name'],'vars':job_vars})
                events=[{'title':n['name'],'start':iso(n['start']),'end':iso(n['end'])} for n in gdata['x']['scheduler']]
                self.xsend_all({'type':'get_schedule','events':events})
            if msg.get('type')=="getCode":
                job=gdata['x']['jobs'].get(msg['name'])
                self.xsend({'type':'getCode','code':job['code']})
            if msg.get('type')=="getVars":
                job=gdata['x']['jobs'].get(msg['name'])
                self.xsend({'type':'getVars','vars':job['vars']})
            if msg.get('type')=="setCode":
                job=gdata['x']['jobs'].get(msg['name'])
                job['code']=msg['code']
                xjob=job.copy()
                xjob['name']=msg['name']
                self.xsend_xall({'type':'job','msg':xjob})
            if msg.get('type')=="setVars":
                job=gdata['x']['jobs'].get(msg['name'])
                job['vars']=msg['vars']
                xjob=job.copy()
                xjob['name']=msg['name']
                self.xsend_xall({'type':'job','msg':xjob})
            if msg.get('type')=="jobs":
                jobs=[{'name':k,'status':v['status']} for k,v in gdata['x']['jobs'].items()]
                self.xsend({'type':'jobs','msg':jobs})
            if msg.get('type')=="job":
                job=gdata['x']['jobs'].get(msg['msg']).copy()
                job['name']=msg['msg']
                self.xsend({'type':'job','msg':job})
            if msg.get('type')=="hosts":
                hosts={'master':gdata['x']['master'], 'servers':gdata['x']['servers']} 
                self.xsend({'type':'hosts','msg':hosts})
            if msg.get('type')=="name":
                if msg["old"]=='New Job':
                    gdata['x']['jobs'][msg['new']]={'vars':'','code':'','history':[],'status':1}
                else:
                    job=gdata['x']['jobs'].pop(msg['old'])
                    gdata['x']['jobs'][msg['new']]=job
                    print(f'Change job name from {msg["old"]} to {msg["new"]}')
            if msg.get('type')=="build":
                job=gdata['x']['jobs'].get(msg['name']).copy()
                job_vars=gdata['imports']['executor'].run(job['vars'],gdata,{},-1)
                job_vars.pop('run_id')
                job_vars=[{'name':k,'value':v,'type':tiper.get(type(v),'xzchto')} for k,v in job_vars.items()]
                self.xsend({'type':'build','msg':job_vars})
        except:
            print(self.data)
            traceback.print_exc()

    def connected(self):
        print(f'WebSocket connected: {self.address}')
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

