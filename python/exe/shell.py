from subprocess import Popen,PIPE
from uuid import uuid4

def shell(cmd):
    bat_file=f'{uuid4()}.bat'
    with open(bat_file,'w') as f:
        f.write(cmd)
    with Popen(bat_file, stdout=PIPE) as p:
        while p.returncode is None:
            line=p.stdout.readline()
            if line:print(line.decode('cp866').strip())
            else:break
if __name__ == '__main__':
    shell('''ping 127.0.0.1''')