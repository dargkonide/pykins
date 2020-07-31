import os
import traceback
from time import sleep

# def 

def work(data):
    while 1:
        try:
            sleep(1)
        except:
            with open('err.log','a') as ff:
                traceback.print_exc()
                traceback.print_exc(file=ff)