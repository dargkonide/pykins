from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
from json import loads,dumps
from time import sleep
from threading import Thread

def run(client):
    i=0
    while 1:
        client.sendMessage(dumps({'type':'jobList','message':f'hi {i}'}))
        i+=1
        sleep(0.01)

class SimpleEcho(WebSocket):

    def handleMessage(self):
        # echo message back to client
        print(self.data)

    def handleConnected(self):
        print(self.address, 'connected')
        Thread(target=run,args=(self,)).start()
        

    def handleClose(self):
        print(self.address, 'closed')





server = SimpleWebSocketServer('0.0.0.0', 8123, SimpleEcho)
server.serveforever()