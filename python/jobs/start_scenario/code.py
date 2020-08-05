from socket import gethostbyname
from requests import get
from datetime import datetime
from exe.mysql import *


controllers=['tvsi-erib0031']

controller_path={}
controller_path["tksi-erib0108"]="C:\\hp\\hppch\\bin\\Wlrun.exe"
controller_path["tvsi-erib0021"]="C:\\hp\\hppch\\bin\\Wlrun.exe"
controller_path["tvsi-erib0031"]="C:\\hp\\hppch\\bin\\Wlrun.exe"


get(f'https://tvsi-erib0054:8123/properties?run=803&stend={stend}',auth=('eriblt','1qaz@WSX'),verify=False)#Подготовка бд

with connect('test') as con:
    #Получаем список генераторов
    resp=select(con,"select generator_name from generators_groups where `group`='%s'"%(group.upper()))
    generators=[gethostbyname(n[0]) for n in resp]
    controller=controllers[0]
    links=generators+[gethostbyname(controller)]#список для линковки


with node('tvli-erib0703'):
    from os import popen

    # Выгрузка датапулов
    output=popen(f"""
        cd /opt/data/var/git/{stend}/Datapools
        git reset --hard
        git clean -xfd
        git pull -f 
        git checkout "{branchDatapools}"
        git pull origin "{branchDatapools}"
        chmod -R 777 *
        chown -R root:root *
    """).read()
    print(output)

    # Выгрузка скриптов
    output=popen(f"""
        cd /opt/data/var/git/{stend}/ERIB_LTScripts
        git reset --hard
        git clean -xfd
        git pull -f 
        git checkout "{branchLTScripts}"
        git pull -f origin "{branchLTScripts}"
        chmod -R 777 *
        chown -R root:root *
    """).read()
    print(output)
    
    if stend=='NT2':
        output=popen(f"sed -i 's/8088/8188/g' /opt/data/var/git/NT2/Datapools/NT2/Influx/InfluxAuth.txt").read()
        print(output)


    # линковка
    for it in links:
        dir_pool= "//${it}/git"
        # создаём директорию для конкретного IP для создания в ней симлинки
        output=popen(f"""
            cd /opt/data/var/generators
            if [ ! -d "{it}" ];  then
                mkdir {it}
                chmod -R 777 {it}                
            fi
        """).read()

        # удаляем симлинки, если они есть
        output=popen(f"""
            cd /opt/data/var/generators/"{it}"
            if [ -d datafiles ]; then unlink datafiles; fi
            if [ -d ERIBScripts ]; then unlink ERIBScripts; fi
        """).read()

        # создаём симлинки на НТ1 или НТ2
        output=popen(f"""
            cd /opt/data/var/generators/{it}
            ln -s /opt/data/var/git/{stend}/Datapools/{stend} datafiles
            ln -s /opt/data/var/git/{stend}/ERIB_LTScripts  ERIBScripts
        """).read()

print('Start test')
with node(controller):
    from importlib import util
    from random import randint
    import sys
    
    def println(*args,**kwargs):
        print(*args,**kwargs)

    sys.path.insert(1,r'//TVSI-ERIB0054/auto/scenario_generate/')
    spec=util.spec_from_file_location('scenario_generate',"//TVSI-ERIB0054/auto/scenario_generate/scenario_generate_ci.py")
    x=util.module_from_spec(spec)
    
    xid=randint(10000000,100000000)
    vars(x).update({'xid':xid,
        'stend':stend,
        'generators_group':group,
        'scenario_id':scenario_id,
        'selected_test':scheduler,
        'profile_percentage':profile_percentage,
        'target_comment':target_comment,
        'skip_pending':skip_pending,
        'disable_transactions':disable_transactions,
        'print':println})
    spec.loader.exec_module(x)

with connect() as con:
    xlinks=controller+':'+group
    start_time=datetime.now()
    branch=branchLTScripts+':'+branchDatapools
    test_id=select(con,"select id from tests_registry where links='%s'"%xid)[0][0]
    insert(con,"update tests_registry set links=%s, start_time=%s, branch=%s, target_comment=%s, `user`=%s, compare_test_path=%s, properties=%s where id=%s",\
        [[xlinks,start_time,branch,target_comment,user,M_TEST,properties_scheduler,test_id]])
    rows = select(con,f"select scenario_name,result_path from eriblt_reestr_tests.tests_registry where id={test_id}")[0]
    if jira_comment:
        issue=jira_comment.split(" ")[0]
        insert(con,"insert into jira_comment(id,issues,commented) values(%s,%s,%s)",[[test_id,issue,0]])
    test_path,result_path=rows

with node(controller):
    from os import popen
    wl_path=controller_path[controller]
    output=popen(f"""taskkill /f /t /im wlrun.exe""").read()
    output=popen(f"""python //TVSI-ERIB0054/auto/full_control/core.py \"{wl_path}\" {test_id}""").read()
    print(output.encode('utf-8').decode('cp1251'))