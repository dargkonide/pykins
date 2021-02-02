with node("tkli-erib0124"):
    from cx_Oracle import connect as cxconnect
    from cx_Oracle import makedsn
    from threading import Thread
    from time import sleep,time
    import pymqi
    

    template='<GetDpanByPanRq><RqUID>00000000000000000000000000000348</RqUID><RqTm>2020-09-25T12:45:59.999999999</RqTm>{0}</GetDpanByPanRq>'
    templpan='<Pans><PanID>{0}</PanID><PanValue>{1}</PanValue></Pans>'

    conects={'NT2':
    {'erib':('m6eriblt-2.cgs.sbrf.ru','1521','eriblt2','srb_tech',xsecret),
    'csa':('m6eriblt-4.cgs.sbrf.ru','1525','eribcsalt2','srb_tech_csa',xsecret),
    'logs':('m6eriblt-4.cgs.sbrf.ru','1522','eribloglt2','log_ikfl',xsecret)}
    ,'NT1':
    {'standin':('m6esalt-4.cgs.sbrf.ru','1521','eribstlt','SRB_IKFL_S',xsecret),
    'erib':('m6eriblt-1.cgs.sbrf.ru','1521','eriblt1','srb_tech',xsecret),
    'csa':('m6eriblt-3.cgs.sbrf.ru','1525','eribcsalt1','srb_tech_csa',xsecret),
    'logs':('m6eriblt-3.cgs.sbrf.ru','1522','eribloglt1','log_ikfl',xsecret)}}
    
    def query(con,sql):
        c=con.cursor()
        resp=c.execute(sql)
        resp=c.fetchall()
        c.close()
        return resp

    def insert(con,qinsert,rows):
        c=con.cursor()
        c.executemany(qinsert,rows)
        con.commit()
        c.close()

    def connect(params):
        dns=makedsn(params[0],params[1],params[2])
        return cxconnect(user=params[3],password=params[4],dsn=dns,encoding='UTF-8')

    def send():
        md=pymqi.MD()
        md.ReplyToQ=b'ERIB.PAN.RESPONSE'
        qmgr=pymqi.connect('M99.INTCS.LT.GATEWAY','DEV.SVRCONN','10.53.161.5(2002)')
        putq=pymqi.Queue(qmgr,'ESB.PAN.REQUEST')
        pans=[]
        for i,n in pan.items():
            if not dpan.get(i):
                pans.append((i,n))
                if len(pans)>=int(send_count):
                    msg=template.format(''.join([templpan.format(i,n) for i,n in pans]))
                    pans.clear()
                    while 1:
                        try:
                            putq.put(msg,md)
                            break
                        except Exception as e:
                            print('send',e)
                            sleep(1)
        if len(pans)>0:
            msg=template.format(''.join([templpan.format(i,n) for i,n in pans]))
            pans.clear()
            putq.put(msg,md)

    def parse(msg):
        # print(msg)
        upload=[]
        for i,n in enumerate(msg.split(b'Dpans')):
            if i%2:
                dpan_id=n.split(b'DpanID')[1][1:-2].decode('utf-8')
                dpan_value=n.split(b'DpanValue')[1][1:-2].decode('utf-8')
                dpan[dpan_id]=dpan_value
                upload.append([dpan_value,pan[int(dpan_id)]])
        return upload

    def upload_dpan(con,asd):
        print(f'upload {len(asd)} rows')
        t=time()
        insert(con,f"UPDATE {table} SET DPAN = :1 where PAN = :2",asd)
        print(f'uploaded {time()-t} sec.')

    def recv(con,a):
        con=connect(conects[stend][name])
        print('oracle connected')
        gmo=pymqi.GMO()
        gmo.Options=pymqi.CMQC.MQGMO_WAIT | pymqi.CMQC.MQGMO_FAIL_IF_QUIESCING
        gmo.WaitInterval=5000
        qmgr=pymqi.connect('M99.INTCS.LT.GATEWAY','DEV.SVRCONN','10.53.161.5(2002)')
        print('recv mq connected')
        getq=pymqi.Queue(qmgr,'ERIB.PAN.RESPONSE')
        print('recv queue opened')
        upload=[]
        while len(dpan)<len(pan):
            # print(len(dpan))
            try:
                md=pymqi.MD()
                message=getq.get(None,md,gmo)
                upload+=parse(message)
            except Exception as e:
                print('recv:',e,a.is_alive())
                print(len(dpan),'/',len(pan))
                if not a.is_alive():
                    break
                # if not a.is_alive():
                #     a=Thread(target=send)
                #     a.start()
            if len(upload)>=int(upload_count):
                print(len(dpan),'/',len(pan))
                upload_dpan(con,upload)
                upload.clear()
        if len(upload)>0:
            print(len(dpan),'/',len(pan))
            upload_dpan(con,upload)
            upload.clear()
        getq.close()
        con.close()
    
    
    
    while 1:
        pan,dpan={},{}
        stend,name=bd.split()
        con=connect(conects[stend][name])
        print('Started loading pans')
        for i,(xpan,xdpan) in enumerate(query(con,f"select /*+parallel(128)*/ * from (select PAN,DPAN from {table} where DPAN IS NULL and length(pan) in (14,15,16,18)) where rownum<={download_count}")):
            if xpan and xpan.isdigit():
                lpan=len(xpan)
                if lpan==16 or lpan==15 or lpan==14 or lpan==18:
                    pan[i]=xpan
        print(f'Pans loaded: {len(pan)}')
        if not pan:break

        con.close()
        a=Thread(target=send)
        b=Thread(target=recv,args=(con,a))
        a.start()
        b.start()
        a.join()
        b.join()
    del pan
    del dpan