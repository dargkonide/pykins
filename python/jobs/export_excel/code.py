from threading import Thread
from datetime import datetime
from pymysql import connect as myconnect
from xlrd import open_workbook
from json import loads
from os import environ
from re import sub
import os


def connect(bd='servers'):
    return myconnect('10.53.139.133','root',mssql_password,bd,\
        charset='utf8mb4')

def select(con,sql):
    c=con.cursor()
    c.execute(sql)
    r=c.fetchall()
    c.close()
    return r

def insert(con,sql,params):
    c=con.cursor()
    c.executemany(sql,params)
    con.commit()
    c.close()



def sp_export(sp):
    con=connect()
    x=select(con,"select * from sp_nodes")
    last_id=set(n[4] for n in x)
    new_id=set(n[4] for n in sp)
    new_ids=list(new_id-last_id)
    last=set(n[1:] for n in x)
    new=set(tuple(n[1:]) for n in sp)
    changed=[n[3] for n in list(last-new)]
    max_id=max(n[0] for n in x or [[0]])+1
    if new_ids:
        new_sp=[list(n[1:]) for n in sp if n[4] in new_ids]
        new_sp=[[max_id+i]+n for i,n in enumerate(new_sp)]
        insert(con,"Insert into sp_nodes (id,stend,console,clusters,servers,ip,app,groups,host,kluster) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",new_sp)
    if changed:
        chd_sp=[list(n[1:4])+list(n[5:])+list(n[4:5]) for n in sp if n[4] in changed]
        insert(con,"update sp_nodes set stend=%s,console=%s,clusters=%s,ip=%s,app=%s,groups=%s,host=%s,kluster=%s where SERVERS=%s",chd_sp)
    x=select(con,"select id,stend,console,clusters,servers,ip,app,groups,host,kluster from sp_nodes")
    max_id=select(con,"select max(id)+1 from sp_map")
    max_id=max_id and max_id[0][0] or 1
    snid=[(m[0],n[6]) for n in sp for m in x if n[4]==m[4]]
    snid.sort()
    smap=[(max_id,n[0],n[1],datetime.now()) for n in snid]
    insert(con,"Insert into sp_map (id,snid,app,idate) values (%s,%s,%s,%s)",smap)

def mq_export(mq):
    con=connect()
    x=select(con,"select * from mq_nodes")
    last_id=set(n[2] for n in x)
    new_id=set(n[2] for n in mq)
    new_ids=list(new_id-last_id)
    last=set(n[1:] for n in x)
    new=set(tuple(n[1:]) for n in mq)
    changed=[n[1] for n in list(last-new)]
    max_id=max(n[0] for n in x or [[0]])+1
    if new_ids:
        new_mq=[list(n[1:]) for n in mq if n[2] in new_ids]
        new_mq=[[max_id+i]+n for i,n in enumerate(new_mq)]
        insert(con,"insert into mq_nodes (id,stend,servers,ip,ke,comm,qm,port,channel,host,kluster) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",new_mq)
    if changed:
        chd_mq=[[n[1]]+list(n[3:])+[n[2]] for n in mq if n[2] in changed]
        insert(con,"update mq_nodes set stend=%s,ip=%s,ke=%s,comm=%s,qm=%s,port=%s,channel=%s,host=%s,kluster=%s where servers=%s",chd_mq)
    x=select(con,"select id,stend,servers,ip,ke,comm,qm,port,channel,host,kluster from mq_nodes")
    max_id=select(con,"select max(id)+1 from mq_map")
    max_id=max_id and max_id[0][0] or 1
    mnid=[(m[0],n[5]) for n in mq for m in x if n[2]==m[2]]
    mnid.sort()
    mmap=[(max_id,n[0],n[1],datetime.now()) for n in mnid]
    insert(con,"insert into mq_map(id,mnid,comm,idate) values (%s,%s,%s,%s)",mmap)

sp,mq=[],[]
stends={'nt1':'NT1','нт1':'NT1','нт2':'NT2','нт3':'NT3','nt2':'NT2','nt3':'NT3'}
filtr=['Расчет','Перезаливка','Заглушки','Этап2.СП']
rb=open_workbook(os.path.join(excel_path,excel_name))
# mapping=loads(open('export_servers/mapping.json').read())
keys=set(mapping.keys())
# print(dir(rb))

for n in rb.sheet_names():#Получаем сервера из excel
    if n in filtr:continue
    sheet=rb.sheet_by_name(n)
    slist=[]
    for m in range(sheet.nrows):
        row=[str(r).strip() for r in sheet.row_values(m)]
        slist.append(row)
    last=''
    stend=[stends[m] for m in stends.keys() if m in n.lower()]
    stend=stend and stend[0] or ''
    if 'сп' in n.lower() and stend:
        for x in range(1,3):
            for m in slist:
                if m[x]:last=m[x]
                else:m[x]=last
        for i,m in enumerate(slist):
            if i:
                for x in range(len(m)):
                    m[x]=sub(r'[^A-Za-z0-9._-]','',str(m[x])) # Удаление лишних символов
                    if not m[x]:m[x]=None
                if m[6] in keys:m[5]=mapping[m[6]] # Приведение имен приложений к одному виду
                sp.append([i,stend]+m[1:9])
                if debug:print(sp[-1])
        # print(m[1:8])

    if 'mq' in n.lower() and stend:
        j=0
        for i,m in enumerate(slist):
            if i and m[1] and m[2]:
                m[6]=str(m[6]).replace('.0','')
                mq.append([j,stend]+m[1:10])
                if debug:print(mq[-1])
                j+=1
    if 'sowa' in n.lower():
        for i,s in enumerate(slist):
            stend=[stends[m] for m in stends.keys() if m in s[4].lower()]
            stend=stend and stend[0] or ''
            if stend:
                sp.append([i,stend,s[0],'StandAlone',s[0],s[2],s[4],'_'.join([stend.lower(),'SOWA']),None,None])
                if debug:print(sp[-1])


t=[Thread(target=sp_export,args=(sp,)),Thread(target=mq_export,args=(mq,))]
for n in t:n.start()
for n in t:n.join()

run_job("pmi_config", {'stend':'ALL'}, wait=False)