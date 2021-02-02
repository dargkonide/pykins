from exe.mysql import *


with connect('eriblt_reestr_tests') as con:
    pref=[n[0] for n in select(con,"select type from tests_registry where class='ERIB'")]
    pref={n:pref.count(n) for n in set(pref)}
    
    stend = ['NT1','NT2']
    group = [n[0] for n in select(con,"select distinct `group` from test.generators_groups")]
    scenario_id = [n[0] for n in select(con,"select distinct id from profiles_info order by id desc")]
    branchLTScripts = 'master'
    branchDatapools = 'master'
    scheduler = [n[0] for n in select(con,"select distinct name from schedulers")]
    scheduler.sort(key=lambda x:pref.get(x,0),reverse=True)# Сортировка по популярности
    profile_percentage = '100'
    target_comment = 'НТ1 надежность'
    test_time = True
    influx_drop = True
    skip_pending = True
    disable_transactions = False
    wait_shd = False
    M_TEST = ''
    jira_comment = ''
    properties_scheduler = ''
    user = 'khudyakov1-ad'
    del pref