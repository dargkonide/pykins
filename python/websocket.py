from simple_websocket_server import WebSocketServer, WebSocket
from json import loads,dumps
from time import sleep
from dateutil import parser
from threading import Thread
from random import randint
from datetime import datetime,timedelta
import traceback

iso=lambda x:datetime.fromtimestamp(x).isoformat()
tsp=lambda x:parser.parse(x).timestamp()

tiper={int:'string',str:'string',list:'select',tuple:'multiselect',bool:'checkbox'}
class SimpleEcho(WebSocket):

    def xsend(self,msg):
        self.send_message(dumps(msg))
        # print(f"Send: {msg}")

    def xsend_all(self,msg):
        for n in clients:
            n.send_message(dumps(msg))
        # print(f"Send all: {msg}")

    def xsend_xall(self,msg):
        for n in clients:
            if self!=n:
                n.send_message(dumps(msg))
        # print(f"Send xall: {msg}")

    def handle(self):
        try:
            msg=loads(self.data)
            print(f"Receive: {msg}")
            if msg.get('type')=="unsubscribe":
                print(f"Receive: {msg}")
                if msg['msg']=="getCode":
                    self.gdata['imports']['loader'].q.put(1)
                if msg['msg']=="getVars":
                    self.gdata['imports']['loader'].q.put(1)


            if msg.get('type')=="scheds":
                self.send_message(self.gdata['x']['scheduler'])
            if msg.get('type')=="schedule":
                self.gdata['x']['scheduler'].append({'time':msg['time'],'name':msg['name'],'vars':msg['vars']})
            if msg.get('type')=="get_schedule":
                # TODO: n['date']
                events=[{'id':n['id'],'title':f"#{n['id']} {n['name']}",'start':iso(n['start']),'end':iso(n['end'])} for n in self.gdata['x']['scheduler']]
                self.xsend({'type':'get_schedule','events':events})
            if msg.get('type')=="schedule_select":
                job=self.gdata['x']['jobs'].get(msg['name'])
                run_id=str(job['last_build_id'])
                job['last_build_id']+=1
                job_vars={n['name']:n.get('select') or n.get('selected') or n['value'] for n in msg['vars']}
                scheduler=self.gdata['x']['scheduler']
                scheduler.append({'id':run_id,'start':tsp(msg['start']),'end':tsp(msg['end']),'name':msg['name'],'vars':job_vars})
                events=[{'id':n['id'],'title':f"#{n['id']} {n['name']}",'start':iso(n['start']),'end':iso(n['end'])} for n in scheduler]
                self.xsend_all({'type':'get_schedule','events':events})
            if msg.get('type')=="schedule_delete":
                scheduler=self.gdata['x']['scheduler']
                [scheduler.remove(n) for n in scheduler.copy() if n['id']==msg['id'] and n['name']==msg['name']]
                events=[{'id':n['id'],'title':f"#{n['id']} {n['name']}",'start':iso(n['start']),'end':iso(n['end'])} for n in scheduler]
                self.xsend_all({'type':'get_schedule','events':events})
            if msg.get('type')=="schedule_move":
                scheduler=self.gdata['x']['scheduler']
                [n.update({'start':tsp(msg['start']),'end':tsp(msg['end'])}) for n in scheduler.copy() if n['id']==msg['id'] and n['name']==msg['name']]
                events=[{'id':n['id'],'title':f"#{n['id']} {n['name']}",'start':iso(n['start']),'end':iso(n['end'])} for n in scheduler]
                self.xsend_xall({'type':'get_schedule','events':events})
            if msg.get('type')=="getCode":
                self.lastname=msg['name']
                job=self.gdata['x']['jobs'].get(msg['name'])
                self.xsend({'type':'getCode','code':job['code']})
            if msg.get('type')=="getVars":
                self.lastname=msg['name']
                job=self.gdata['x']['jobs'].get(msg['name'])
                self.xsend({'type':'getVars','vars':job['vars']})
            if msg.get('type')=="setCode":
                self.lastname=msg['name']
                job=self.gdata['x']['jobs'].get(msg['name'])
                job['code']=msg['code']
                xjob=job.copy()
                xjob['name']=msg['name']
                self.xsend_xall({'type':'job','msg':xjob})
            if msg.get('type')=="setVars":
                self.lastname=msg['name']
                job=self.gdata['x']['jobs'].get(msg['name'])
                job['vars']=msg['vars']
                xjob=job.copy()
                xjob['name']=msg['name']
                self.xsend_xall({'type':'job','msg':xjob})
            if msg.get('type')=="jobs":
                jobs=[{'name':k,'status':v['status']} for k,v in self.gdata['x']['jobs'].items()]
                self.xsend({'type':'jobs','msg':jobs})
            if msg.get('type')=="job":
                self.lastname=msg['msg']
                job=self.gdata['x']['jobs'].get(msg['msg']).copy()
                job['name']=msg['msg']
                self.xsend({'type':'job','msg':job})
            if msg.get('type')=="hosts":
                hosts={'master':self.gdata['x']['master'], 'servers':self.gdata['x']['servers']} 
                self.xsend({'type':'hosts','msg':hosts})
            if msg.get('type')=="name":
                if msg["old"]=='New Job':
                    self.gdata['x']['jobs'][msg['new']]={'vars':'','code':'','history':{},'status':1,'last_build_id':1}
                else:
                    job=self.gdata['x']['jobs'].pop(msg['old'])
                    self.gdata['x']['jobs'][msg['new']]=job
                    print(f'Change job name from {msg["old"]} to {msg["new"]}')
            if msg.get('type')=="build":
                self.lastname=msg['name']
                job=self.gdata['x']['jobs'].get(msg['name']).copy()
                job_vars=self.gdata['imports']['executor'].run(job['vars'],self.gdata,{},-1,msg['name'])
                job_vars.pop('run_id')
                job_vars.pop('job_name')
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
def work(data):
    server = WebSocketServer('0.0.0.0', 5123, SimpleEcho, data)
    server.serve_forever()

