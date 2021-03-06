from simple_websocket_server import WebSocketServer, WebSocket
from json import loads,dumps
from time import sleep
from dateutil import parser
from threading import Thread
from random import randint
from datetime import datetime,timedelta
from uuid import uuid4
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
            if self is not n:
                n.send_message(dumps(msg))
                # print(f"Send: {msg}")

    def get_events(self,name):
        events=[]
        for n in self.gdata['x']['scheduler']:
            if n['name']==name:
                events.append({
                    'id':n['id'],
                    'title':f"#{n['id']} {n['name']}",
                    'start':iso(n['start']),
                    'end':iso(n['end'])
                })
        return events

    def get_calendar_events(self):
        events=[]
        for n in self.gdata['x']['scheduler']:
            events.append({
                'id':f"{n['id']}{n['name']}",
                'title':f"#{n['id']} {n['name']}",
                'start':iso(n['start']),
                'end':iso(n['end'])
            })
        return events

    def get_event_integration(self,name):
        events=[]
        for n in self.gdata['x']['scheduler']:
            if n['name']==name:
                events.append({
                    'id':n['id'],
                    'title':f"#{n['id']} {n['name']}",
                    'start':iso(n['start']),
                    'end':iso(n['end']),
                    'vars':n['vars']
                })
        return events

    def handle(self):
        try:
            msg=loads(self.data)
            print(f"Receive: {msg}")
            if msg.get('type')=="auth_token":
                if users.get(msg.get('token')):
                    self.user=users[msg['token']]
                else:
                    self.xsend({'type':'auth_token','auth':False})
                return

            if msg.get('type')=="authenticate":
                self.user=msg['user']
                token=str(uuid4())
                users[token]=msg['user']
                self.xsend({'type':'authenticate', 'msg': { 'id': '1', 'username': msg['user'], 'role': 'admin', 'token': token}})
                #self.xsend({'type':'authenticate', 'error': 'user dont exist'})

            if not hasattr(self, 'user'):return

            if msg.get('type')=="unsubscribe":
                # print(f"Receive: {msg}")
                if msg['msg']=="getCode":
                    self.gdata['imports']['loader'].q.put(1)
                if msg['msg']=="getVars":
                    self.gdata['imports']['loader'].q.put(1)
                if msg['msg']=="glu":
                    self.gdata['imports']['logs'].qsend.setdefault(self.lastname_run_id,[]).remove(self)
                    

            if msg.get('type')=="get_schedule_integrations":
                self.xsend(self.get_event_integration('start_scenario'))

            if msg.get('type')=="set_schedule_integrations":
                job=self.gdata['x']['jobs'].get('start_scenario')
                run_id=str(job['last_build_id'])
                job['last_build_id']+=1
                self.gdata['x']['scheduler'].append({'id':run_id,'start':tsp(msg['start']),'end':tsp(msg['end']),'name':'start_scenario','vars':msg['vars']})
                self.xsend_all({'type':'get_schedule','events':self.get_events('start_scenario')})

            if msg.get('type')=="get_schedule":
                # TODO: n['date']
                self.xsend({'type':'get_schedule','events':self.get_events(msg['name'])})

            if msg.get('type')=="get_calendar":
                # TODO: n['date']
                self.xsend({'type':'get_calendar','events':self.get_calendar_events()})

            if msg.get('type')=="schedule_select":
                job=self.gdata['x']['jobs'].get(msg['name'])
                run_id=str(job['last_build_id'])
                job['last_build_id']+=1

                job_vars={}
                for n in msg['vars']:
                    if n.get('select') is not None:
                        job_vars[n['name']]=n.get('select')
                    elif n.get('selected') is not None:
                        job_vars[n['name']]=n.get('selected')
                    else: 
                        job_vars[n['name']]=n['value'] 

                scheduler=self.gdata['x']['scheduler']
                scheduler.append({'id':run_id,'start':tsp(msg['start']),'end':tsp(msg['end']),'name':msg['name'],'vars':job_vars})
                self.xsend_all({'type':'get_schedule','events':self.get_events(msg['name'])})

            if msg.get('type')=="schedule_delete":
                scheduler=self.gdata['x']['scheduler']
                [scheduler.remove(n) for n in scheduler.copy() if n['id']==msg['id'] and n['name']==msg['name']]
                self.xsend_all({'type':'get_schedule','events':self.get_events(msg['name'])})

            if msg.get('type')=="schedule_move":
                scheduler=self.gdata['x']['scheduler']
                [n.update({'start':tsp(msg['start']),'end':tsp(msg['end'])}) for n in scheduler.copy() if n['id']==msg['id'] and n['name']==msg['name']]
                self.xsend_xall({'type':'get_schedule','events':self.get_events(msg['name'])})

            if msg.get('type')=="getCode":
                self.lastname=msg['name']
                job=self.gdata['x']['jobs'].get(msg['name'])
                self.xsend({'type':'getCode','code':job['code']})

            if msg.get('type')=="getVars":
                self.lastname=msg['name']
                job=self.gdata['x']['jobs'].get(msg['name'])
                self.xsend({'type':'getVars','vars':job['vars']})

            if msg.get('type')=="getLogs":
                self.lastname=msg['name']
                run_id=f"{msg['id']}{msg['name']}"
                logs=self.gdata['logs'][run_id]
                self.xsend({'type':'getLogs','logs':'\n'.join(logs)})

            if msg.get('type')=="glu":
                run_id=f"{msg['id']}{msg['name']}"
                self.lastname_run_id=run_id
                self.gdata['imports']['logs'].qsend.setdefault(run_id,[]).append(self)

            if msg.get('type')=="setCode":
                self.lastname=msg['name']
                job=self.gdata['x']['jobs'].get(msg['name'])
                job['code']=msg['code']
                self.xsend_xall({'type':'getCode','code':job['code']})

            if msg.get('type')=="setVars":
                self.lastname=msg['name']
                job=self.gdata['x']['jobs'].get(msg['name'])
                job['vars']=msg['vars']
                self.xsend_xall({'type':'getVars','vars':job['vars']})

            if msg.get('type')=="jobs":
                folder=['jobs']+msg.get('folder')
                last_folder=self.gdata['x']['root']
                for n in folder:
                    last_folder=last_folder.get(n)
                jobs=[]
                for n in last_folder:
                    if not last_folder.get(n):
                        job={'name':n,'type':'job'}
                        name='\\'.join(folder+[n])
                        history=self.gdata['x']['jobs'][name]['history']
                        if history:
                            job.update(history[str(max(int(n) for n in history.keys()))])
                        jobs.append(job)
                    else:
                        jobs.append({'name':n,'type':'folder'})
                
                # jobs=[{'name':k } for k,v in self.gdata['x']['jobs'].items()]
                # for job in jobs:
                #     history=self.gdata['x']['jobs'][job['name']]['history']
                #     if history:
                #         job.update(history[str(max(int(n) for n in history.keys()))])
                # print(self.gdata['x']['scheduler'])
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
                job_vars=self.gdata['imports']['executor'].process.run(job['vars'],self.gdata,{},-1,msg['name'])
                job_vars.pop('run_id')
                job_vars.pop('job_name')
                job_vars=[{'name':k,'value':v,'type':tiper.get(type(v),'xzchto')} for k,v in job_vars.items()]
                self.xsend({'type':'build','msg':job_vars})

            if msg.get('type')=="delete":
                self.gdata['x']['jobs'].pop(msg['name'])

            

# TODO: Подписка на обновление шедулера
            if msg.get('type')=="history":
                job=self.gdata['x']['jobs'].get(msg['name'])
                history=[{'id':k,'status':v['status'],'start':v.get('start',''),'end':v.get('end',''),'delta':v.get('delta','')} for k,v in job['history'].items()]
                for k in self.gdata['x']['scheduler']:
                    if k['name'] == msg['name']:
                        history.append({'id':k['id'],'status':'sheduled','start':iso(k['start']),'end':iso(k['end'])})
                print(history)
                self.xsend({'type':'history','msg':history})
                self.gdata['imports']['executor'].qhistory.setdefault(msg['name'],[]).append(self)
            if msg.get('type')=='stop':
                print(msg)
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
users={}
def work(data):
    server = WebSocketServer('0.0.0.0', 5124, SimpleEcho, data)
    server.serve_forever()

