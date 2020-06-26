from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
from json import loads,dumps
from time import sleep
from threading import Thread
from random import randint
import traceback


def run(client):
    print("Started")
    i=0
    while 1:
        client.sendMessage(dumps({'type':'jobList','message':f'hi {i}',\
            'table':[{'name':f'job{i}','status':'pass'} for j,n in enumerate(range(100000))]}))
        i+=1
        sleep(1)
        break

class SimpleEcho(WebSocket):

    def handleMessage(self):
        try:

            msg=loads(self.data)
            print(msg)
            if msg.get('type')=="jobs":
                jobs=[{'name':k,'status':v['status']} for k,v in gdata['x']['jobs'].items()]
                print(jobs)
                self.sendMessage(dumps({'type':'jobs','msg':jobs}))
            if msg.get('type')=="job":
                job=gdata['x']['jobs'].get(msg['msg'])
                self.sendMessage(dumps({'type':'job','msg':job}))
        except:
            print(self.data)
            traceback.print_exc()

    def handleConnected(self):
        print(self.address, 'connected')
        # Thread(target=run,args=(self,)).start()
        

    def handleClose(self):
        print(self.address, 'closed')

gdata=None
def work(data):
    global gdata
    gdata=data
    server = SimpleWebSocketServer('0.0.0.0', 8123, SimpleEcho)
    server.serveforever()

