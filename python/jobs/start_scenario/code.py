from exe.mysql import *
from datetime import datetime
from requests import get
from time import sleep


controller_path={}
controller_path["tksi-erib0108"]="C:\\hp\\hppch\\bin\\Wlrun.exe"
controller_path["tvsi-erib0021"]="C:\\hp\\hppch\\bin\\Wlrun.exe"
controller_path["tvsi-erib0031"]="C:\\hp\\hppch\\bin\\Wlrun.exe"
controller_path["tvsi-erib0032"]="C:\\hp\\hppch\\bin\\Wlrun.exe"

print('RunID:',run_id)
while 1:
    r=get('http://tvsi-erib0054:8193/',params={'build_id':f'start_scenario_{run_id}'})
    if r.text[0]=='e':
        print(r.text.split(':')[1])
        sleep(15)
    else:
        links=r.text.split()[3]
        controller=r.text.split()[2]
        print(controller)
        break

run_job("prepare_stend", {'stend':stend,'clean_log':True}, wait=False)

run_job('pull_datapools',{
    "stend":stend,
    "branchDatapools":branchDatapools,
    "branchLTScripts":branchLTScripts,
    "datapools":True,
    "ltscripts":True
})

run_job('link_unlink',{"stend":stend,"servers":links,"local":False})


print('Generate scenario')
with node(controller):
    from random import randint
    import os
    
    xid=randint(10000000,100000000)
    os.environ['STEND']=str(stend)
    os.environ['PREFIX']=f'{xid}|||pykins'
    os.environ['GENERATORS_GROUP']=str(group)
    os.environ['SCENARIO_ID']=str(scenario_id)
    os.environ['SCHEDULER']=str(scheduler)
    os.environ['PROFILE_PERCENTAGE']=str(profile_percentage)
    os.environ['SKIP_PENDING']=str(skip_pending)
    os.environ['DISABLE_TRANSACTIONS']=str(disable_transactions)
    
    shell(r'python \\TVSI-ERIB0054\auto\scenario_generate\scenario_generate.py')

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

print('Start test')
with node(controller):
    import os
    wl_path=controller_path[controller]
    os.environ['TEST_TIME']=str(test_time)
    os.environ['INFLUX_DROP']=str(influx_drop)
    os.environ['SKIP_PENDING']=str(skip_pending)
    os.environ['DISABLE_TRANSACTIONS']=str(disable_transactions)
    shell(f"""
        taskkill /f /t /im wlrun.exe
        python //TVSI-ERIB0054/auto/full_control/core.py \"{wl_path}\" {test_id}
    """)

with connect() as con:
    insert(con,"update eriblt_reestr_tests.tests_registry set end_time=%s where id=%s",[[datetime.now(),test_id]])

run_job('collate_results',{"test_id":test_id},wait=False)