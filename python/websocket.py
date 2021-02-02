from simple_websocket_server import WebSocketServer, WebSocket
from datetime import datetime,timedelta
from threading import Thread
from dateutil import parser
from random import randint
from queue import Queue
from json import loads,dumps
from time import sleep,time
from uuid import uuid4
import traceback
import platform

if platform.system()=='Windows':
    from win32security import LogonUser,LOGON32_LOGON_NETWORK,LOGON32_PROVIDER_DEFAULT

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

    def xsend_targets(self,msg,xclients):
        for n in xclients:
            n.send_message(dumps(msg))
            # print(f"Send: {msg}")

    def xsend_xtargets(self,msg,xclients):
        for n in xclients:
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
                    'id':f"#{n['name']}:{n['id']}",
                    # 'title':f"#{n['id']} {n['name']}",
                    'start':iso(n['start']),
                    'end':iso(n['end']),
                    'vars':n['vars']
                })
        return events

    def handle(self):
        try:
            msg=loads(self.data)
            if not 'get_schedule_integrations' in msg.get('type'):
                print(f"{self.user if hasattr(self, 'user') else ''} receive: {msg['type']}")
            if msg.get('type')=="get_runnings":
                builds={}
                for key in self.gdata['running'].keys():
                    f=key.rfind('_')
                    name,run_id=key[:f],key[f+1:]
                    job_vars=self.gdata['x']['jobs'][name]['history'][run_id]['vars']
                    builds[key]=job_vars
                self.xsend({'type':'get_runnings','builds':builds})

            if msg.get('type')=="unsubscribe":
                # print(f"Receive: {msg}")
                if msg['msg']=="getCode":
                    self.gdata['imports']['loader'].q.put(1)
                    if hasattr(self,'lastname') and self in get_code.get(self.lastname,[]):
                        get_code[self.lastname].remove(self)
                if msg['msg']=="getVars":
                    self.gdata['imports']['loader'].q.put(1)
                    if hasattr(self,'lastname') and self in get_vars.get(self.lastname,[]):
                        get_vars[self.lastname].remove(self)
                if msg['msg']=="glu":
                    if hasattr(self,'lastname_run_id'):
                        self.gdata['imports']['logs'].qsend.setdefault(self.lastname_run_id,[]).remove(self)
                if msg['msg']=="get_schedule":
                    if hasattr(self,'lastname') and self in schedule.get(self.lastname,[]):
                        schedule[self.lastname].remove(self)
                if msg['msg']=='history':
                    if hasattr(self,'lastname'):
                        self.gdata['imports']['executor'].qhistory[self.lastname].remove(self)
                
            if msg.get('type')=="auth_token":
                if users.get(msg.get('token')):
                    self.user=users[msg['token']]
                else:
                    self.xsend({'type':'auth_token','auth':False})

            if msg.get('type')=="authenticate":
                if platform.system()=='Windows':
                    try:
                        # token=LogonUser(msg['user'],'ALPHA',msg['pass'],LOGON32_LOGON_NETWORK,LOGON32_PROVIDER_DEFAULT)
                        if msg['user']=='admin' and msg['pass']=='16352302':
                            token=True
                        if token:
                            token=str(uuid4())
                            self.user=msg['user']
                            users[token]=msg['user']
                            self.xsend({'type':'authenticate','msg':{'id':'1','username':msg['user'],'role':'admin','token':token}})
                    except Exception as e:
                        self.xsend({'type':'authenticate','error':e.strerror})
                        print(e.strerror)

            if msg.get('type')=="get_schedule_integrations":
                self.xsend(self.get_event_integration('start_scenario'))

            if msg.get('type')=="set_schedule_integrations":
                job=self.gdata['x']['jobs'].get('start_scenario')
                run_id=str(job['last_build_id'])
                job['last_build_id']+=1
                self.gdata['x']['scheduler'].append({'id':run_id,'start':tsp(msg['start']),'end':tsp(msg['end']),'name':'start_scenario','vars':msg['vars']})
                self.xsend_all({'type':'get_schedule','events':self.get_events('start_scenario')})

            if msg.get('type')=="delete_integration":
                scheduler=self.gdata['x']['scheduler']
                [scheduler.remove(n) for n in scheduler.copy() if n['id']==msg['id'].split(':')[1] and n['name']=='start_scenario']
                self.xsend_all({'type':'get_schedule','events':self.get_events('start_scenario')})

            if msg.get('type')=="move_integration":
                scheduler=self.gdata['x']['scheduler']
                [n.update({'start':tsp(msg['start']),'end':tsp(msg['end'])}) for n in scheduler.copy() if n['id']==msg['id'].split(':')[1] and n['name']=='start_scenario']
                self.xsend_all({'type':'get_schedule','events':self.get_events('start_scenario')})

            if not hasattr(self, 'user'):return


            if msg.get('type')=="get_schedule":
                # TODO: n['date']
                self.lastname=msg['name']
                schedule.setdefault(msg['name'],[]).append(self)
                self.xsend({'type':'get_schedule','events':self.get_events(msg['name'])})

            if msg.get('type')=="get_calendar":
                # TODO: n['date']
                self.xsend({'type':'get_calendar','events':self.get_calendar_events()})

            if msg.get('type')=="runJob":
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

                if self.user:
                    job_vars['user']=self.user

                scheduler=self.gdata['x']['scheduler']
                scheduler.append({'id':run_id,'start':time(),'name':msg['name'],'vars':job_vars})

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

                if self.user:
                    job_vars['user']=self.user

                scheduler=self.gdata['x']['scheduler']
                scheduler.append({'id':run_id,'start':tsp(msg['start']),'end':tsp(msg['end']),'name':msg['name'],'vars':job_vars})
                # self.xsend_all({'type':'get_schedule','events':self.get_events(msg['name'])})
                self.xsend_targets({'type':'get_schedule','events':self.get_events(msg['name'])},schedule.get(msg['name'],[]))

            if msg.get('type')=="schedule_delete":
                scheduler=self.gdata['x']['scheduler']
                [scheduler.remove(n) for n in scheduler.copy() if n['id']==msg['id'] and n['name']==msg['name']]
                # self.xsend_all({'type':'get_schedule','events':self.get_events(msg['name'])})
                self.xsend_targets({'type':'get_schedule','events':self.get_events(msg['name'])},schedule.get(msg['name'],[]))

            if msg.get('type')=="schedule_move":
                scheduler=self.gdata['x']['scheduler']
                [n.update({'start':tsp(msg['start']),'end':tsp(msg['end'])}) for n in scheduler.copy() if n['id']==msg['id'] and n['name']==msg['name']]
                # self.xsend_xall({'type':'get_schedule','events':self.get_events(msg['name'])})
                self.xsend_xtargets({'type':'get_schedule','events':self.get_events(msg['name'])},schedule.get(msg['name'],[]))

            if msg.get('type')=="getCode":
                self.lastname=msg['name']
                get_code.setdefault(msg['name'],[]).append(self)
                job=self.gdata['x']['jobs'].get(msg['name'])
                self.xsend({'type':'getCode','code':job['code']})

            if msg.get('type')=="getVars":
                self.lastname=msg['name']
                get_vars.setdefault(msg['name'],[]).append(self)
                job=self.gdata['x']['jobs'].get(msg['name'])
                self.xsend({'type':'getVars','vars':job['vars']})

            if msg.get('type')=="getLogs":
                self.lastname=msg['name']
                run_id=f"{msg['id']}{msg['name']}"
                if self.gdata['logs'].get(run_id):
                    logs=self.gdata['logs'][run_id]
                    self.xsend({'type':'getLogs','logs':'\n'.join(logs)})
                
            if msg.get('type')=="stop":
                for node in set(self.gdata['x']['jobs'][msg['name']]['history'][msg['id']]['nodes']):
                    print('kill node',node)
                    self.gdata['send'].put((node,{'n':'kill','j':msg['name'],'r':msg['id']},None))

            if msg.get('type')=="glu":
                run_id=f"{msg['id']}{msg['name']}"
                self.lastname_run_id=run_id
                self.gdata['imports']['logs'].qsend.setdefault(run_id,[]).append(self)

            if msg.get('type')=="setCode":
                self.lastname=msg['name']
                job=self.gdata['x']['jobs'].get(msg['name'])
                job['code']=msg['code']
                self.xsend_xtargets({'type':'getCode','code':job['code']},get_code.get(msg['name'],[]))

            if msg.get('type')=="setVars":
                self.lastname=msg['name']
                job=self.gdata['x']['jobs'].get(msg['name'])
                job['vars']=msg['vars']
                # self.xsend_xall({'type':'getVars','vars':job['vars']})
                self.xsend_xtargets({'type':'getVars','vars':job['vars']},get_vars.get(msg['name'],[]))

            if msg.get('type')=="jobs":
                jobs=[{'name':k } for k,v in self.gdata['x']['jobs'].items()]
                for job in jobs:
                    history=self.gdata['x']['jobs'][job['name']]['history']
                    if history:
                        job.update(history[str(max(int(n) for n in history.keys()))])
                # print(self.gdata['x']['scheduler'])
                self.xsend({'type':'jobs','msg':jobs})

            if msg.get('type')=="job":
                self.lastname=msg['msg']
                job=self.gdata['x']['jobs'].get(msg['msg']).copy()
                job['name']=msg['msg']
                self.xsend({'type':'job','msg':job})

            if msg.get('type')=="hosts":
                servers=self.gdata['x']['servers']
                servers.sort()
                hosts={'master':self.gdata['x']['master'], 'servers':servers} 
                self.xsend({'type':'hosts','msg':hosts})

            if msg.get('type')=="name":
                if msg["old"]=='New Job':
                    self.gdata['x']['jobs'][msg['new']]={'vars':'','code':'','history':{},'status':1,'last_build_id':1}
                else:
                    job=self.gdata['x']['jobs'].pop(msg['old'])
                    self.gdata['x']['jobs'][msg['new']]=job

                    import sys
                    print(sys.getsizeof(self.gdata))
                    # from pympler import muppy, summary
                    # a=muppy.get_objects()
                    # s=summary.summarize(a)
                    # summary.print_(s)
                    # print(f'Change job name from {msg["old"]} to {msg["new"]}')

            if msg.get('type')=="build":
                self.lastname=msg['name']
                job=self.gdata['x']['jobs'].get(msg['name']).copy()
                pin,pout=Queue(),Queue(),
                job_vars=self.gdata['imports']['executor'].process.run(job['vars'],(pin,pout),{},-1,msg['name'],'')
                job_vars.pop('run_id')
                job_vars.pop('job_name')
                complete_job_vars=[]
                for k,v in job_vars.items():
                    jvar={'name':k,'value':v,'type':tiper.get(type(v),'xzchto')}
                    if jvar['type']=='select' and v:
                        jvar['select']=v[0]
                    complete_job_vars.append(jvar)
                # job_vars=[{'name':k,'value':v,'type':tiper.get(type(v),'xzchto'),'select':v[0]} for k,v in job_vars.items()]
                self.xsend({'type':'build','msg':complete_job_vars})

            if msg.get('type')=="delete":
                self.gdata['x']['jobs'].pop(msg['name'])

            # TODO: Подписка на обновление шедулера
            if msg.get('type')=="history":
                self.lastname=msg['name']
                job=self.gdata['x']['jobs'].get(msg['name'])
                history=[{'id':k,'status':v['status'],'start':v.get('start',''),'end':v.get('end',''),'delta':v.get('delta','')} for k,v in job['history'].items()]
                for k in self.gdata['x']['scheduler']:
                    if k['name'] == msg['name']:
                        history.append({'id':k['id'],'status':'sheduled','start':iso(k['start']),'end':iso(k['end']) if k.get('end') else None})
                # print(history)
                self.xsend({'type':'history','msg':history})
                self.gdata['imports']['executor'].qhistory.setdefault(msg['name'],[]).append(self)
            
            if msg.get('type')=="history_vars":
                self.lastname=msg['name']
                job=self.gdata['x']['jobs'].get(msg['name'])
                if job:
                    run=job['history'].get(msg['id'])
                    if run:
                        run_vars=run.get('vars')
                        if run_vars:
                            complete_run_vars=[]
                            for k,v in run_vars.items():
                                jvar={'name':k,'value':v,'type':tiper.get(type(v),'xzchto')}
                                if jvar['type']=='select' and v:
                                    jvar['select']=v[0]
                                complete_run_vars.append(jvar)
                            self.xsend({'type':'history_vars','msg':complete_run_vars})
                for n in self.gdata['x']['scheduler']:
                    if n['name']==msg['name'] and n['id']==msg['id']:
                        run_vars=n.get('vars')
                        if run_vars:
                            complete_run_vars=[]
                            for k,v in run_vars.items():
                                jvar={'name':k,'value':v,'type':tiper.get(type(v),'xzchto')}
                                if jvar['type']=='select' and v:
                                    jvar['select']=v[0]
                                complete_run_vars.append(jvar)
                            self.xsend({'type':'history_vars','msg':complete_run_vars})
            if msg.get('type')=="change_vars":
                self.lastname=msg['name']
                for n in self.gdata['x']['scheduler']:
                    if n['name']==msg['name'] and n['id']==msg['id']:
                        job_vars={}
                        for m in msg['vars']:
                            if m.get('select') is not None:
                                job_vars[m['name']]=m.get('select')
                            elif m.get('selected') is not None:
                                job_vars[m['name']]=m.get('selected')
                            else: 
                                job_vars[m['name']]=m['value']
                        n['vars'].update(job_vars)

        except:
            print(self.data)
            traceback.print_exc()

    def connected(self):
        print(f'WebSocket connected: {self.address}')
        clients.append(self)
        # Thread(target=run,args=(self,)).start()

    def handle_close(self):
        if hasattr(self, 'user'):print(self.user,end=' ')
        print(self.address, 'closed')
        clients.remove(self)
        self.gdata['imports']['loader'].q.put(1)


        if hasattr(self,'lastname') and self in get_code.get(self.lastname,[]):
            get_code[self.lastname].remove(self)
        if hasattr(self,'lastname') and self in get_vars.get(self.lastname,[]):
            get_vars[self.lastname].remove(self)
        if hasattr(self,'lastname') and self in schedule.get(self.lastname,[]):
            schedule[self.lastname].remove(self)

        if hasattr(self,'lastname_run_id'):
            self.gdata['imports']['logs'].qsend.setdefault(self.lastname_run_id,[]).remove(self)

        if hasattr(self,'lastname') and self in self.gdata['imports']['executor'].qhistory.get(self.lastname,[]):
            self.gdata['imports']['executor'].qhistory[self.lastname].remove(self)

clients=[]
get_code={}
get_vars={}
schedule={}
users={}
def work(data):
    server = WebSocketServer('0.0.0.0', 5124, SimpleEcho, data)
    server.serve_forever()

