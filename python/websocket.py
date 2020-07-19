from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
from json import loads,dumps
from time import sleep
from threading import Thread
from random import randint
import traceback

class SimpleEcho(WebSocket):

    def handleMessage(self):
        try:
            msg=loads(self.data)
            print(msg)
            if msg.get('type')=="code":
                job=gdata['x']['jobs'].get(msg['name'])
                job['code']=msg['code']
                xjob=job.copy()
                xjob['name']=msg['name']
                print('Send', {'type':'job','msg':xjob})
                [n.sendMessage(dumps({'type':'job','msg':xjob})) for n in clients if n is not self]
            if msg.get('type')=="vars":
                job=gdata['x']['jobs'].get(msg['name'])
                job['vars']=msg['vars']
                xjob=job.copy()
                xjob['name']=msg['name']
                print('Send', {'type':'job','msg':xjob})
                [n.sendMessage(dumps({'type':'job','msg':xjob})) for n in clients if n is not self]
            if msg.get('type')=="jobs":
                jobs=[{'name':k,'status':v['status']} for k,v in gdata['x']['jobs'].items()]
                print('Send', {'type':'jobs','msg':jobs})
                print('=======================')
                print(gdata['x'])
                print('=======================')
                self.sendMessage(dumps({'type':'jobs','msg':jobs}))
            if msg.get('type')=="job":
                job=gdata['x']['jobs'].get(msg['msg']).copy()
                job['name']=msg['msg']
                print('Send', {'type':'job','msg':job})
                self.sendMessage(dumps({'type':'job','msg':job}))
            if msg.get('type')=="hosts":
                hosts={'master':gdata['x']['master'], 'servers':gdata['x']['servers']} 
                print('Send', {'type':'hosts','msg':hosts})
                self.sendMessage(dumps({'type':'hosts','msg':hosts}))
            if msg.get('type')=="name":
                job: dict=gdata['x']['jobs'].pop(msg['old'])
                print(f'Change job name from {msg["old"]} to {msg["new"]}')
                gdata['x']['jobs'][msg['new']]=job
        except:
            print(self.data)
            traceback.print_exc()


    def handleConnected(self):
        print(self.address, 'connected')
        clients.append(self)
        # Thread(target=run,args=(self,)).start()
        

    def handleClose(self):
        print(self.address, 'closed')
        clients.remove(self)

clients=[]
gdata: dict=None
def work(data):
    global gdata
    gdata=data
    server = SimpleWebSocketServer('0.0.0.0', 8123, SimpleEcho)
    server.serveforever()