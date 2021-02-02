from threading import Thread

def work(serv):
    with node(serv):
        from cx_Oracle import connect as cxconnect
        from cx_Oracle import makedsn
        from threading import Thread,Event
        from queue import Queue
        from time import sleep,time
        from random import randint
        from socket import gethostname
        
        server=gethostname()

        conects={'NT2':
        {'standin':['m6esalt-4.cgs.sbrf.ru','1529','eribstlt','SRB_IKFL_S',xsecret],
        'erib':('m6eriblt-2.cgs.sbrf.ru','1521','eriblt2','srb_tech',xsecret),
        'csa':('m6eriblt-4.cgs.sbrf.ru','1525','eribcsalt2','srb_tech_csa',xsecret),
        'logs':('m6eriblt-4.cgs.sbrf.ru','1522','eribloglt2','log_ikfl',xsecret)}
        ,'NT1':
        {'erib':('m6eriblt-1.cgs.sbrf.ru','1521','eriblt1','srb_tech',xsecret),
        'csa':('m6eriblt-3.cgs.sbrf.ru','1525','eribcsalt1','srb_tech_csa',xsecret),
        'logs':('m6eriblt-3.cgs.sbrf.ru','1522','eribloglt1','log_ikfl',xsecret)}}
        
        def query(con,sql):
            c=con.cursor()
            resp=c.execute(sql)
            resp=c.fetchall()
            c.close()
            return resp

        def connect(params):
            dns=makedsn(params[0],params[1],params[2])
            return cxconnect(user=params[3],password=params[4],dsn=dns,encoding='UTF-8')

        def oppener(params,count,x,q):
            params[1]=str(randint(1521,1529))
            sessions=[]
            for n in range(count):
                con=connect(params)
                sessions.append(con)
            q.put(1)
            x.wait()
            for con in sessions: con.close()
            # del sessions

        print(server,'start_sessions_open')
        q=Queue()
        x=Event()
        threads=[]
        for n in range(20):
            t=Thread(target=oppener,args=(conects['NT2']['standin'],100,x,q))
            t.start()
            threads.append(t)
        for n in range(20):
            q.get()
        print(server,'sessions_openned')
        sleep(36000)
        print(server,'start_sessions_close')
        x.set()
        print(server,'sessions_closed')
        for n in threads:
            n.join()
        
trds=[]
for server in servers.split(','):
    t=Thread(target=work,args=(server,))
    t.start()
    trds.append(t)
for n in trds:n.join()