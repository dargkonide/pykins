
log = r"\\tvli-erib0703\awrs\log"
# директория с исходниками, откуда забираем собранные дистрибутивы
deploy_source = r"\\10.106.145.88\ERIB_main"
# собираем 1 раз для всех серверов из списка
if operation == 'Deploy':
    print(f"Build maven {name_service}, {stend},  {branch_stubs}")
    with node("tvli-erib0703"):
        shell(f"""
            cd /var/git/ERIB_main
            git reset --hard
            git clean -xfd                
            git pull                
            git checkout {branch_stubs}
            git pull origin {branch_stubs}
            chmod -R 777 *
            
            cd /var/git/ERIB_main/{name_service}
            /opt/apache-maven-3.6.0/bin/mvn clean compile package
            if [ -e settings_{stend}.ini ]
            then
                cp settings_{stend}.ini settings.ini
                chmod 777 settings.ini
            else 
                echo "no file found settings_{stend}.ini"
            fi
        """)

for idx, server in enumerate(servers.strip().replace(' ','').split(',')):
    print(idx)
        
    with node(server):
        from time import sleep
        import traceback
        import platform
        import os

        def is_unix():
            return platform.system()=='Linux'

        def stop(name_service):
            try:
                if is_unix():
                    shell(f"""
                        systemctl daemon-reload
                        systemctl stop {name_service}
                    """)
                else:
                    shell(f"net stop {name_service}")
            except:
                trace=traceback.format_exc()
                print(trace)

        def start(name_service):
            try:
                if is_unix():
                    shell(f"""
                        systemctl daemon-reload
                        systemctl start {name_service}
                    """)
                else:
                    shell(f"net start {name_service}")
            except:
                trace=traceback.format_exc()
                print(trace)

        # удаляем сервис
        def undeploy(deploy_source, name_service):
            if is_unix():
                # затачиваем под mount
                deploy_source = deploy_source.replace('\\','/')
                shell(f"""
                    if mount -v | grep -q /mnt/MQStubsGit
                    then 
                        umount -l /mnt/MQStubsGit
                    fi
                    cd /etc/systemd/system/
                    systemctl disable {name_service}.service && echo "0" || echo "1"
                    
                    if [ -L /etc/systemd/system/{name_service}.service ]
                    then
                        unlink {name_service}.service
                    else
                        rm -f {name_service}.service
                    fi
                    rm -rf /opt/standalone/{name_service}
                    systemctl daemon-reload
                """)
            else:
                try:
                    # сервиса может не существовать
                    try:
                        shell(f"""
                            chcp 1251
                            cd /d "D:\\Distrib\\nssm-2.24\\win64"
                            nssm remove {name_service} confirm
                        """)
                    except:
                        trace=traceback.format_exc()
                        print(trace)
                    
                    shell(f"""
                        chcp 1251
                        IF EXIST "D:\\Distrib\\{name_service}" rmdir /s /q "D:\\Distrib\\{name_service}"
                    """)
                except:
                    trace=traceback.format_exc()
                    print(trace)
                
        # устанавливаем сервис
        def deploy(deploy_source, name_service):
            if is_unix():
                # затачиваем под mount
                deploy_source = deploy_source.replace('\\','/')
                shell(f"""
                    if ! [ -d /mnt/MQStubsGit ]
                    then 
                        mkdir /mnt/MQStubsGit
                    fi
                    mount -t cifs {deploy_source} -o username=eriblt,password={password} /mnt/MQStubsGit

                    if ! [ -d /opt/standalone ]
                    then 
                        mkdir /opt/standalone
                    fi

                    mkdir /opt/standalone/{name_service}
                    cp -f -R /mnt/MQStubsGit/{name_service}/{name_service}.service /opt/standalone/{name_service}/
                    cp -f -R /mnt/MQStubsGit/{name_service}/settings.ini /opt/standalone/{name_service}/
                    cp -f -R /mnt/MQStubsGit/{name_service}/target/{name_service}.jar /opt/standalone/{name_service}/
                    cd /etc/systemd/system/

                    systemctl enable /opt/standalone/{name_service}/{name_service}.service
                    systemctl daemon-reload
                    systemctl restart {name_service}
                """)
            else:
                try:
                    shell(f"""
                        chcp 1251
                        mkdir "D:\\Distrib\\{name_service}"
                        
                        cd /d "D:\\Distrib\\{name_service}"
                        robocopy "{deploy_source}\\{name_service}" "D:\\Distrib\\{name_service}" Start.bat settings.ini
                        robocopy "{deploy_source}\\{name_service}\\target" "D:\\Distrib\\{name_service}" "{name_service}.jar"
                        dir
                        cd /d "D:\\Distrib\\nssm-2.24\\win64"

                        nssm.exe install {name_service} "D:\\Distrib\\{name_service}\\Start.bat"
                        nssm.exe set {name_service} AppDirectory "D:\\Distrib\\{name_service}"
                        nssm.exe get {name_service} AppDirectory

                        cd /d "D:\\Distrib\\nssm-2.24\\win64"
                        rem nssm.exe status {name_service}        
                    """)
                except:
                    trace=traceback.format_exc()
                    print(trace)    
        if operation != "Restart_ALL":
            print(f"{name_service} {operation} {server}")
            if operation=="Deploy":
                if name_service=="WAY4Stub" or name_service=="ERIB_WAY4":
                    print(idx)
                    print("Файл для изменения: {deploy_source}\\{name_service}\\settings.ini")
                    MQservers = ['tvli-erib1223', 'tvli-erib1224', 'tvli-erib1225', 'tvli-erib1226'] if is_unix() else \
                        ['tv-erib-8r2-509', 'tv-erib-8r2-510', 'tv-erib-8r2-511', 'tv-erib-8r2-512', 'tv-erib-8r2-611', 'tv-erib-8r2-612','ahto1','ahto2','ahto3','ahto4']
                    with open("{deploy_source}\\{name_service}\\settings.ini") as fileConf:
                        confPropLine = fileConf.readlines()
                    #переменная для изменения в конфиге
                    varInput = "MQ_HostName1"
                    # правим переменную в массиве
                    for i,it in enumerate(confPropLine):
                        if varInput in it:
                            confPropLine[i] = f"<MQ_HostName1>{MQservers[idx]}</string>"
                            print(confPropLine[i])
                    # записываем обратно в конфиг изменённый массив
                    with open("{deploy_source}\\{name_service}\\settings.ini",'w') as fileConf:
                        for it in confPropLine:
                            fileConf.write(f"{it}{os.linesep}")     
                if name_service=="WAY4Stub_Linux" or name_service=="ERIB_WAY4_Linux":
                    print(idx)
                    print(f"Файл для изменения: {deploy_source}\\{name_service}\\settings.ini")
                    if stend == "NT1": MQservers = ['tvli-erib2103','tvli-erib2104','tvli-erib2105','tvli-erib2106']
                    if stend == "NT2": MQservers = ['tvli-erib1223','tvli-erib1224','tvli-erib1225','tvli-erib1226']        
                    # изменяем конфиг для каждого второго сервера way4
                    if idx % 3 == 0:
                        # читаем данные в массив
                        with open("{deploy_source}\\{name_service}\\settings.ini") as fileConf:
                            confPropLine = fileConf.readlines()
                        #переменная для изменения в конфиге
                        varInput = "MQ_HostName1"
                        # правим переменную в массиве
                        for i,it in enumerate(confPropLine):
                            if varInput in it:
                                confPropLine[i] = f"<MQ_HostName1>{MQservers[int(idx/3)]}</string>"
                                print(confPropLine[i])
                        # записываем обратно в конфиг изменённый массив
                        with open("{deploy_source}\\{name_service}\\settings.ini",'w') as fileConf:
                            for it in confPropLine:
                                fileConf.write(f"{it}{os.linesep}")
                stop(name_service)
                sleep(1)
                undeploy(deploy_source, name_service)
                deploy(deploy_source, name_service)
                start(name_service)        
            elif operation=="Restart":
                stop(name_service)
                sleep(1)
                start(name_service)
            elif operation=="Stop":
                stop(name_service)
            elif operation=="Start":
                start(name_service)
            elif operation=="GetLog":
                try:
                    if is_unix():
                        shell(f"""
                            cd /opt/Tomcat\\ 7.0/logs
                            mkdir /mnt/Log_Tomcat/{server}
                            cp /opt/Tomcat\\ 7.0/logs/* /mnt/Log_Tomcat/{server}
                        """)
                    else:
                        shell(f"""
                            cd /d "C:\\Program Files\\Apache Software Foundation\\Tomcat 7.0\\logs"
                            mkdir {log}\\{server}
                            robocopy /e . {log}\\{server}
                        """)
                except:
                    trace=traceback.format_exc()
                    print(trace)
            elif operation=="Remove_service":
                stop(name_service)
                sleep(1)
                undeploy(deploy_source, name_service)
        else:
            print(f"{operation}  {server}")
            if operation=="Restart_ALL":
                for idxz, name_services in enumerate(all_services.strip().replace(' ','').split(',')):
                    stop(name_services)
                    sleep(1)
                    start(name_services)
