nodes={

    'NT1':'tvsi-erib0001',

    'NT2':'tvsi-erib0052'

}



secret=secret.encode('utf-8')

standart=standart.encode('utf-8')

mssql=mssql.encode('utf-8')

mysql=mysql.encode('utf-8')

tomcat=tomcat.encode('utf-8')

old=old.encode('utf-8')



with node(nodes[stend]):

    import os

    from time import sleep



    types={'.cfg','.conf','.json','.xml'}



    def replace(k,v):

        for a,b,c in os.walk('D:/'):

            for n in c:

                if any(m in n for m in types):

                    with open(os.path.join(a,n),'br') as f:

                        x=f.read()

                    if k in x:

                        print(n)

                        with open(os.path.join(a,n),'bw') as f:

                            f.write(x.replace(k,v))



    if stend=='NT1':

        shell('''

            net stop OracleDBMonitoring

            net stop TopActivity

            net stop PMI

            net stop MBKMonitoring

            net stop MSSQLMonitoring_fork

            net stop "Telegraf Data Collector Service"'''

        )

        replace(b'{password}',secret)

        replace(b'{std_password}',standart)

        replace(b'{mssql_password}',mssql)

        replace(b'{mysql_creds}',mysql)

        replace(b'password = "{tomcat_password}"',tomcat)

        shell('''

            net start OracleDBMonitoring

            net start TopActivity

            net start PMI

            net start MBKMonitoring

            net start MSSQLMonitoring_fork

            net start "Telegraf Data Collector Service"'''

        )

        sleep(30)

        replace(secret,b'{password}')

        replace(standart,b'{std_password}')

        replace(mssql,b'{mssql_password}')

        replace(mysql,b'{mysql_creds}')

        replace(tomcat,b'password = "{tomcat_password}"')

    else:

        shell('''

            net stop DBtoInflux

            net stop DBtoInflux_x86

            net stop TopActivity_CSA

            net stop TopActivity_ERIB

            net stop TopActivity_LOG

            net stop TopActivity_x86

            net stop PMI

            net stop MSSQLMonitoring_MBK

            net stop "Telegraf Data Collector Service"'''

        )

        replace(b'{password}',secret)

        replace(b'{std_password}',standart)

        replace(b'{mssql_password}',mssql)

        replace(b'{mysql_creds}',mysql)

        replace(b'password = "{tomcat_password}"',tomcat)

        replace(b'{old_password}',old)

        shell('''

            net start DBtoInflux

            net start DBtoInflux_x86

            net start TopActivity_CSA

            net start TopActivity_ERIB

            net start TopActivity_LOG

            net start TopActivity_x86

            net start PMI

            net start MSSQLMonitoring_MBK

            net start "Telegraf Data Collector Service"'''

        )

        sleep(30)

        replace(secret,b'{password}')

        replace(standart,b'{std_password}')

        replace(mssql,b'{mssql_password}')

        replace(mysql,b'{mysql_creds}')

        replace(tomcat,b'password = "{tomcat_password}"')

        replace(old,b'{old_password}')