from requests import get
from json import loads

r=get(f'http://10.53.139.133:808{stend[-1]}/c').text
m=loads(r.replace("'",'"'))

if not transactions:
    print('Доступные для отключения транзакции:')
    for n in m:
        print(n)
else:
    z={m[n.strip()]:int(set_transactions) for n in transactions.split(',') if m.get(n.strip())}
    print(z)
    r=get(f'http://10.53.139.133:808{stend[-1]}/b',params=z).text
    print(r)