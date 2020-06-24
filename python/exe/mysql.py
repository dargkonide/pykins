from pymysql import connect as myconnect

class connect:
    def __init__(self,bd='eriblt_reestr_tests'):
        self.bd=bd
    def __enter__(self):
        self.conn=myconnect('10.53.139.133','root','test',self.bd,charset='utf8mb4')
        return self.conn
    def __exit__(self, type, value, traceback):
        self.conn.close()

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

