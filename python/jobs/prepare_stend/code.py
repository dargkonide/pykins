from threading import Thread
import sys
import os

shell('''
    git clone git@sbt-gitlab.ca.sbrf.ru:ERIB/JenkinsScript.git
    cd JenkinsScript
    git add --all
    git reset --hard
    git pull
''')

config={
    'NT1':{
        'erib':('srb_ikfl','erib_m6'),
        'csa':('csa_ikfl','csa_m6'),
        'logs_erib':('log_ikfl','log_m6_x86'),
        'logs_csa':('csa_log_ikfl','log_m6_x86')
    },
    'NT2':{
        'erib':('srb_ikfl','erib_lt2_m6'),
        'csa':('csa_ikfl','csa_lt2_m6'),
        'logs_erib':('log_ikfl','log_lt2_m6'),
        'logs_csa':('csa_log_ikfl','log_lt2_m6')
    }
}

threads=[]
os.chdir('JenkinsScript/Prepare_LT_enviroment')

print(f"{stend}: подготовка БД ЕРИБ")
username,sid=config.get(stend).get('erib')
cmd=f'sqlplus.exe "{username}"/"{passwd}"@{sid} @block_prepare.sql'
threads.append(Thread(target=shell,args=(cmd,)))

print(f"{stend}: подготовка БД ЦСА")
username,sid=config.get(stend).get('csa')
cmd=f'sqlplus.exe "{username}"/"{passwd}"@{sid} @CSA_prepare.sql'
threads.append(Thread(target=shell,args=(cmd,)))

if clean_log:
    print(f"{stend}: Чистка логов ЕРИБ")
    username,sid=config.get(stend).get('logs_erib')
    cmd=f'sqlplus.exe "{username}"/"{passwd}"@{sid} @log_prepare_erib.sql'
    threads.append(Thread(target=shell,args=(cmd,)))

    print(f"{stend}: Чистка логов ЦСА")
    username,sid=config.get(stend).get('logs_csa')
    cmd=f'sqlplus.exe "{username}"/"{passwd}"@{sid} @log_prepare_csa.sql'
    threads.append(Thread(target=shell,args=(cmd,)))

for n in threads:n.start()
for n in threads:n.join()