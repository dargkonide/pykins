with node(start_on_node):
    from subprocess import check_call
    from pymysql import connect as myconnect
    from threading import Thread
    from socket import socket,gethostbyname,setdefaulttimeout
    from os.path import isfile
    from os import mkdir,environ,remove
    import ssl

    setdefaulttimeout(10)

    collector="""        <collector>
                <ssl-enabled>true</ssl-enabled>
                <host>{0[0]}</host>
                <port>{0[1]}</port>
                <username>eriblt</username>
                <password>{1}</password>
                <tags>
                    <tag name="App">{0[2]}</tag>
                </tags>
            </collector>"""

    conf="""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
    <configuration 
        xmlns="influxdb-agent-was" 
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="influxdb-agent-was config.xsd">
        <influxdb>
            <url>{0}</url>
            <database>{1}</database>
            <username/>
            <password/>
            <submit-interval-sec>15</submit-interval-sec>
        </influxdb>
        <keystores>
            <keystore>
                <trust-store-path>{2}</trust-store-path>
                <trust-store-password>{3}</trust-store-password>
            </keystore>
        </keystores>
        <collectors>
    {4}
        </collectors>
    </configuration>"""

    def dump_cer(host,port):
        try:
            x=ssl.get_server_certificate((host,port))
            with open(certs+'%s.cer'%host,'wb') as f:
                f.write(ssl.PEM_cert_to_DER_cert(x))
        except:
            print('Err dump:',host,port)

    def check_port(n):
        for m in ports:
            try:
                x=ssl.get_server_certificate((n[0],m))
                with open(certs+'%s.cer'%n[0],'wb') as f:
                    f.write(ssl.PEM_cert_to_DER_cert(x))
                pas.append((n[0],m,n[1]))
                print('pass',n[0],m)
                break
            except Exception as e:
                pass
                # print('err',n[0],m)

    def read(con):
        buf=b''
        while buf[-3:]!=b'<~>':
            try:data=con.recv(4096)
            except:break
            if data:buf+=data
            else:break
        z=loads(buf[:-3])
        return z

    def send(con,x):
        con.send(dumps(x,2)+b'<~>')

    def connect(bd='servers'):
        return myconnect('10.53.139.133','root',mysql_password,bd,\
            charset='utf8mb4')

    def select(con,sql):
        c=con.cursor()
        c.execute(sql)
        r=c.fetchall()
        c.close()
        return r

        



    config=[]
    ws=[]

    con=connect()#Получаем сервера из MySQL
    x=select(con,"select server_name,application from servs where stand='%s'"%(stand))
    for n in x:
        ws.append(n[0])
        config.append(n)


    try:mkdir(certs)#Получаем сертификаты
    except:pass
    pas=[]
    threads=[]
    ports=[8880,8879,8881,8882]
    for n in config:#Подбираем ws api порт
        try:
            t=Thread(target=check_port,args=(n,))
            t.start()
            threads.append(t)
        except:
            pass
    for n in threads:n.join()
    #threads=[]
    #for n in ws:
    #    t=Thread(target=dump_cer,args=(n,9043))
    #    t.start()
    #    threads.append(t)
    #for n in threads:n.join()
    try:remove(keystore_path)
    except:pass
    for n in ws:#Импортируем сертификаты
        if isfile(certs+'%s.cer'%n):
            x=[jdk_path, 
            '-import', '-alias', n,
            '-file', certs+'%s.cer'%n,
            '-keystore', keystore_path,
            '-storepass', trust_store_password, '-noprompt']
            try:check_call(x)
            except Exception as e:
                print('ERROR append sertificate from:',n,e)


    collectors=[collector.format(n,trust_store_password) for n in pas]#Собираем конфиг
    config=conf.format(url,database,trust_store_path,trust_store_password,'\n'.join(collectors))
    with open(config_path,'w',encoding='utf-8') as f:
        f.write(config)

    shell(f'powershell -command "Restart-Service {service_name} -Force"')
