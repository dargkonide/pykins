import os
import io
import zipfile
from time import sleep
from threading import Thread

zio=io.BytesIO()

folder_filtr=['ui','logs','__pycache__']
file_type_white_list=['.py','.json']
file_filter=["__lock__"]
abspath=os.path.abspath('../../')
old_cwd=os.getcwd()
os.chdir(abspath)

zf=zipfile.ZipFile(zio, 'w', zipfile.ZIP_DEFLATED) #zip bin master 
for a,b,c in os.walk('.'):
    if not any(n in a for n in folder_filtr):
        print(a,b,c)
        zf.write(a)
        for n in c:
            if any(m in n for m in file_type_white_list) and not any(m in n for m in file_filter):
                zf.write(os.path.join(a,n))
        
os.chdir(old_cwd)
zf.close()
zio.seek(0)
zip_file=zio.read()
del zio

print(len(zip_file))

def work(server):
    with node(server):
        print(len(zip_file))
        import io
        import os
        import shutil
        import zipfile
        import platform
        

        old_cwd=os.getcwd() #save current directory path
        while not 'core.py' in os.listdir('.'): #goto bin directory
            os.chdir('../')

        for filename in os.listdir('.'): #clear current directory     
            try:os.remove(filename)
            except:pass
            try:shutil.rmtree(filename)
            except:pass

        zf=zipfile.ZipFile(io.BytesIO(zip_file))#extract zip
        for n in zf.namelist():
            print(n)
        zf.extractall()

        if platform.system()=='Windows':
            shell('taskkill /f /t /im pythonw.exe')
            shell('powershell -command "Restart-Service pykins -Force"')
        else:
            shell('systemctl restart pykins')
        
        
        print(os.listdir('.'))
        os.chdir(old_cwd)

for n in servers.split(','):
    Thread(target=work,args=(n.strip(),)).start()
sleep(5)