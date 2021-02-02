import sys 
sys.path.insert(1,'../../../utils')
import mysql
import sqlparse
import traceback
from ora_connect import *

def dc(val):
    if "'" in val[0] and "'" in val[-1]:
        return val[1:-1]
    return val

def ext(val):
    return val[val.find('(')+1:val.rfind(')')]


def check(sql,stend,db):
    z=sqlparse.parse(sql)[0].tokens
    z=[str(n) for n in z if str(n).strip()]

    if str(z[0]).lower()=='update':
        x=dict(map(lambda x:x.split('='),z[3].split(',')))
        x={k.strip():v.strip() for k,v in x.items()}
        keys=list(x.keys())
        select=f'select {",".join(keys)} from {z[1]} {z[4].replace(";","")}'
        if debug:print(select)
        with ora_connect(dconects.get(stend).get(db.lower())) as con:
            for n in set(query(con,select)):
                return int(all(x[keys[i]][1:-1]==m for i,m in enumerate(n))),select
        return 0,select

    if str(z[0]).lower()=='insert':
        if 'values' in z[3].lower():
            table=z[2].split()[0]
            keys=[n.strip() for n in ext(z[2]).split(',')]
            values=[n.strip() for n in ext(z[3]).split(',')]
            x=dict(zip(keys,values))
            where=' and '.join([f'{k}={v}' for k,v in zip(keys,values)])
            select=f'select {",".join(keys)} from {table} where {where}'
            if debug:print(select)
            with ora_connect(dconects.get(stend).get(db.lower())) as con:
                for n in set(query(con,select)):
                    return int(all(x[keys[i]][1:-1]==m for i,m in enumerate(n))),select
            return 0,select

        
con=mysql.connect('properties')

z=mysql.select(con,"select i.id,i.status_nt1,i.status_nt2,p.db,p.sql_on,p.sql_off from property_info as i inner join (select max(id) as mid,pid from property_info group by pid) as x on x.mid=i.id inner join property as p on i.id=p.id")
for pid,status_nt1,status_nt2,db,sql_on,sql_off in z:
    try:
        # print(pid,status_nt1,status_nt2,db)#,sql_on,sql_off)
        on_status_nt1,select_on_nt1=check(sql_on,'NT1',db)
        off_status_nt1,select_off_nt1=check(sql_off,'NT1',db)
        on_status_nt2,select_on_nt2=check(sql_on,'NT2',db)
        off_status_nt2,select_off_nt2=check(sql_off,'NT2',db)
        if status_nt1!=on_status_nt1:
            print(select_on_nt1)
            print(f'#{pid} NT1 status does not match')
        if status_nt2!=on_status_nt2:
            print(select_on_nt2)
            print(f'#{pid} NT2 status does not match')

        if update and on_status_nt1 is not None and status_nt1!=on_status_nt1:
            mysql.insert(con,f'update property_info set status_nt1=%s where id=%s',[[on_status_nt1,pid]])
        if update and on_status_nt2 is not None and status_nt2!=on_status_nt2:
            mysql.insert(con,f'update property_info set status_nt2=%s where id=%s',[[on_status_nt2,pid]])
    except:
        if debug:traceback.print_exc()
    