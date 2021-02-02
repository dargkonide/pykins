from requests import Session
import requests.packages.urllib3 as u
from json import dumps
from datetime import datetime
u.disable_warnings(u.exceptions.InsecureRequestWarning)
s=Session()



def auth():
    s.get(f'https://{host[block]}/ufs-sm/',verify=False)
    form={'username': username,
    'password': password,
    'login-form-type': 'pwd'}
    r=s.post(f'https://{host[block]}/pkmslogin.form',verify=False,data=form)
    print(r.url)

def get_conf(param,path,tenant_code=None):
    results=[]
    s.post(f'https://{host[block]}/ufs-params-manager/rest/application/session',verify=False)
    json={"page":{"pageNumber":0,"pageSize":20,"sort":[]},"filter":{"name":param,"roles":[]}}
    r=s.post(f'https://{host[block]}/ufs-params-manager/rest/parameter/list',json=json,verify=False)
    resp=r.json()
    if resp.get('success') and resp['success'] and resp.get('body'):
        for n in resp['body'].get('parameters',[]):
            print(n['id'],n.get('name'),n.get('description'))
            json={"filter":{"parameterId":n['id'],"isRegex":True,"statuses":["PRESENT","FUTURE"]},"page":{"pageNumber":0,"pageSize":5,"sort":[{"property":"groupCode","direction":"ASC"}]}}
            r=s.post(f'https://{host[block]}/ufs-params-manager/rest/parameter/value/list',json=json,verify=False)
            resp=r.json()
            if resp.get('success') and resp['success'] and resp.get('body'):
                for v in resp['body'].get('bundles',[]):
                    vpath={m['code']:m.get('value','') for m in v.get('path',[]) if m.get('code')}
                    print(vpath,vpath==path)
                    if not path or vpath==path:
                        if v.get('status'):v.pop('status')
                        results.append((n['id'],v))
                    for m in v['values']:
                        print(m['id'],m['value'])
    return results

def get_conf2(param,path,tenant_code=None):
    results=[]
    s.post(f'https://{host[block]}/ufs-config-manager/rest/application/session',verify=False)
    json={"page":{"pageNumber":0,"pageSize":20,"sort":[]},"filter":{"name":param,"roles":[]}}
    r=s.post(f'https://{host[block]}/ufs-config-manager/rest/parameter/list',json=json,verify=False)
    resp=r.json()
    if resp.get('success') and resp['success'] and resp.get('body'):
        for n in resp['body'].get('parameters',[]):
            print(n['id'],n.get('tenantCode'),n.get('name'),n.get('description'))
            if tenant_code and n.get('tenantCode')!=tenant_code:
                continue
            json={"filter":{"parameterId":n['id'],"withHistory":False,"path":[],"value":{}},"page":{"pageNumber":0,"pageSize":5}}
            r=s.post(f'https://{host[block]}/ufs-config-manager/rest/parameter/bundle/list',json=json,verify=False)
            resp=r.json()
            if resp.get('success') and resp['success'] and resp.get('body'):
                for v in resp['body'].get('bundles',[]):
                    vpath={m['code']:m.get('value','') for m in v.get('path',[]) if m.get('code')}
                    print(vpath,vpath==path)
                    if not path or vpath==path:
                        results.append((n['id'],v))
                    for m in v['values']:
                        print(n['id'],v['id'],m)
    return results

def edit(id,old_bundle,new_value):
    json={
      "parameterId": id,
      "oldBundle": old_bundle,
      "newBundle": {
        "groupCode": old_bundle['groupCode'],
        "path": old_bundle['path'],
        "startDate": datetime.now().isoformat()[:-3]+'+0300',
        "values": [new_value]
      }
    }
    try:
        r=s.post(f'https://{host[block]}/ufs-params-manager/rest/parameter/value/edit',json=json,verify=False,timeout=5)
        resp=r.json()
        print(resp)
    except:
        pass

def edit2(id,bundle,new_value):
    json={
      "parameterId": id,
      "bundle": {
        "path": bundle["path"],
        "values": [new_value]
      }
    }
    try:
        r=s.post(f'https://{host[block]}/ufs-config-manager/rest/parameter/value/add',json=json,verify=False,timeout=5)
        resp=r.json()
        print(resp)
    except:
        pass

exe_get_conf={'1.0':get_conf,'2.0':get_conf2}
exe_edit={'1.0':edit,'2.0':edit2}

auth()
for k,v in config[stend].items():
    for i,j in v.items():
        result=exe_get_conf[k](i,j.get('filtr',{}),j.get('tenant_code'))
        if result:
            for id,bundle in result:
                exe_edit[k](id,bundle,j['value'])
# result=get_conf('ufs.baseurl.eribsessioninfo',{'SEGMENT': 'PRIVATE', 'SECTOR': 'PRO-SBOL', 'FIELD': 'p2', 'SUBSYSTEM': 'SM_UKO'})
# if result:
#     for id,bundle in result:
#         edit(id,bundle,bundle['values'][0]['value'])
# result=get_conf('erib.rest.limitsexec.path',{})
# if result:
#     for id,bundle in result:
#         edit(id,bundle,bundle['values'][0]['value'])
# result=get_conf('p2bpayment.erib.url',{})
# if result:
#     for id,bundle in result:
#         edit(id,bundle,bundle['values'][0]['value'])
# result=get_conf2('ufs.baseurl.eribsessioninfo',{'SUBSYSTEM': 'SM_UKO', 'CHANNEL': ''},'SBOL')
# if result:
#     for id,bundle in result:
#         edit2(id,bundle['path'],bundle['values'][0])