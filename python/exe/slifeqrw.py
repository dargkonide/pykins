from time import sleep
from threading import Thread

def test(a):
    b=[a,a,a,a]

while 1:
    Thread(target=test,args=([1,2,3,4]*10,)).start()