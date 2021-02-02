for server in servers.split(','):
    print(server)
    with node(server):
        # from os.path import isdir,isfile,dirname,join
        # from os import popen
        # service_name=popen('powershell -command "Get-Service  | select Name" | find /i "jen"').read().strip()
        # print('finded service name:',service_name)
        # executable_path=popen(f'sc qc "{service_name}"').read().split('BINARY_PATH_NAME   : "')[1].split('"')[0]
        # dir_name=dirname(executable_path)
        # print('finded dir name:',dir_name)
        # if isdir(dir_name):
        #     file_path=join(dir_name,"jenkins-slave.xml")
        #     if isfile(file_path):
        #         config=[]
        #         with open(file_path) as f:
        #             for n in f:
        #                 if '<executable>' in n:
        #                     n='  <executable>java</executable>'
        #                 config.append(n)
        #         # print('\n'.join(config))
        #         with open(file_path,'w') as f:
        #             f.write('\n'.join(config))
        #         print('fixed config')

        #         shell(f'powershell -command "Restart-Service \\"{service_name}\\" -Force"')
        #         print('slave restarted')

        # with open()
        # from os import popen
        # jdk_path='C:\\Program Files\\Java\\jdk1.8.0_281\\bin'
        # shell('"\\\\tvli-erib0703.ca.sbrf.ru\\awrs\\install_java\\jdk-8u281-windows-x64.exe" /s')
        # path=popen('powershell -command "[Environment]::GetEnvironmentVariable(\\"PATH\\",[System.EnvironmentVariableTarget]::Machine)"').read()[:-1]
        # path=';'.join([jdk_path]+[n for n in path.split(';') if not 'jdk1' in n])
        # shell(f'powershell -command "[Environment]::SetEnvironmentVariable(\\"PATH\\", \\"{path}\\", [System.EnvironmentVariableTarget]::Machine)"')
        # shell(f'powershell -command "[Environment]::SetEnvironmentVariable(\\"JAVA_HOME\\", \\"{jdk_path}\\", [System.EnvironmentVariableTarget]::Machine)"')
        # print(popen('java -version').read())