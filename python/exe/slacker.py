from time import sleep,time
import tracemalloc
import traceback

def work(data):
    tracemalloc.start()
    while 1:
        try:
            snap=tracemalloc.take_snapshot()
            for i,stat in enumerate(snap.statistics('filename')[:5],1):
                print(i,stat)
            for i,n in enumerate(snap.statistics('traceback')[:5],1):
                print(i,'_'*50)
                for line in n.traceback.format():
                    print(line)

        except:
            with open('err.log','a') as ff:
                traceback.print_exc()
                traceback.print_exc(file=ff)
        sleep(15)