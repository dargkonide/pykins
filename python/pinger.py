from threading import Thread
from exe.proto import *
from queue import Queue
from time import sleep,time
import traceback
import socket

def work(data):
    while 1:
        try:
            if data['x']['master']!=data['host']:
                data['send'].put((data['x']['master'],{'n':'ping'},None))
        except:
            with open('err.log','a') as ff:
                traceback.print_exc()
                traceback.print_exc(file=ff)
        sleep(5)