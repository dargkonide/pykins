from threading import Thread

from time import sleep



def work(n):

    with node(n):

        shell('shutdown /r /f')



for n in servers.split(','):

    Thread(target=work,args=(n,)).start()



sleep(5)