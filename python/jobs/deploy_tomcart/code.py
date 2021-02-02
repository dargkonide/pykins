
name_service = "Tomcat7"
#directoryStubAar = "\\\\sbt-oat-005\\D\$\\Share1\\Zaglushki\\Deploy\\Tomcat_axis"
directoryStubAar = "D:\\Zaglushki\\Tomcat_axis"
nameStubAar = "ERIB_STUBS_I"
sec_dir = "\\\\sbt-oat-005\\D\$\\Share1\\Zaglushki\\Deploy\\sec_axis"
directoryLog= "\\\\sbt-oat-005\\D\$\\Share1\\Zaglushki\\log"


if "Deploy_war" in operation:
    with node("tvli-erib0703"):
        import traceback
        shell(f"""
            cd /var/git/ERIB_main
            git reset --hard
            git clean -xfd                
            git pull                
            git checkout {service_branch}
            git pull origin {service_branch}
            chmod -R 777 *
            
            cd /var/git/ERIB_main/{service}
            /opt/apache-maven-3.6.0/bin/mvn clean compile package
        """)
        for it in servers.strip().replace(' ','').split(','):
            print(f"{operation} {name_service} {it}")
            try:
                shell(f'''                
                    curl -T "/var/git/ERIB_main/{service}/target/{service}.war" "http://admin:{tomcat}@{it}:8084/manager/text/deploy?path=/{service}&update=true"            
                ''')
            except:
                trace=traceback.format_exc()
                print(trace)


#fileAar = new File(directoryStubAar)?.listFiles()?.toList()
#nameStubAar = TomcatMove.getNameStubAar(fileAar,directoryStubAar)

#Сервера передаются параметром в Job через зяпятую

#забираем aar
# stage("stash AAR from 203 tachki") {
#     dir('D:\\TMP\\Zaglushki\\Deploy') {
#         stash name: "aar-stash", includes: "Tomcat_axis/*"
#     }
# }

# if(!operation.contains("Deploy_war"))
    # servers.trim().replace(' ','').tokenize(',').each{
    for it in servers.strip().replace(' ','').split(','):
        with node(it):
            # /*stage("unstash {it}") {
            #     bat """
            #         rd /s /q "D:\\Zaglushki"
            #         mkdir "D:\\Zaglushki"
            #     """
            #     dir('D:\\Zaglushki') {
            #         unstash "aar-stash"
            #     }
            # }*/
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

            def deploy_axis(deploy_source,deploy_aar):
                try:
                    if is_unix():
                        shell(f"""
                            if ! [ -d /mnt/Deploy_Tomcat_axis ]
                            then 
                                mkdir /mnt/Deploy_Tomcat_axis
                            fi                
                            if ! df -h | grep Deploy_Tomcat_axis 
                            then 
                                mount -t cifs //10.106.145.88/awrs/Deploy/Tomcat_axis -o username=eriblt,password={password} /mnt/Deploy_Tomcat_axis/
                            fi
                            cp -f /mnt/Deploy_Tomcat_axis/{deploy_aar}.aar /opt/Tomcat\\ 7.0/webapps/axis2/WEB-INF/services/
                        """)
                    else:
                        shell(f"""
                            cd /d "C:\\Program Files\\Apache Software Foundation\\Tomcat 7.0\\webapps\\axis2\\WEB-INF\\services"
                            
                            for /f "tokens=1* delims=" %%a in ('date /T') do set datestr=%%a
                            IF NOT EXIST ".\\backup" mkdir ".\\backup"
                            IF NOT EXIST ".\\backup\\stubs-%datestr%" mkdir ".\\backup\\stubs-%datestr%"

                            xcopy /Y /D . ".\\backup\\stubs-%datestr%"
                            dir ".\\backup\\stubs-%datestr%"
                            cd /d "C:\\Program Files\\Apache Software Foundation\\Tomcat 7.0\\webapps\\axis2\\WEB-INF\\services"
                            robocopy /E "{deploy_source}" .
                            if %ERRORLEVEL% EQU 0 echo NoChange
                            if %ERRORLEVEL% EQU 1 echo OkCopy
                            if %ERRORLEVEL% EQU 2 echo XTRA
                            if %ERRORLEVEL% EQU 3 echo OkCopy+XTRA            
                        """)
                    
                except:
                    trace=traceback.format_exc()
                    print(trace)

            print(f"{operation} {name_service} {it}")
            if operation=="Restart":
                stop(name_service)
                sleep(1)
                start(name_service)
            elif operation=="Clean":
                try:
                    if is_unix():
                        shell(f"""
                            rm -rf /opt/Tomcat\\ 7.0/logs/*
                            rm -rf /opt/Tomcat\\ 7.0/temp/*
                            rm -rf /opt/Tomcat\\ 7.0/webapps/backup/*
                            rm -f /var/log/messages-*
                            > /var/log/messages
                        """)
                    else:
                        shell(f"""
                            cd /d "C:\\Program Files\\Apache Software Foundation\\Tomcat 7.0\\logs"
                            Del *.* /a /s /q /f
                            cd /d "C:\\Program Files\\Apache Software Foundation\\Tomcat 7.0\\temp"
                            Del * /a /s /q /f
                            cd /d "C:\\Program Files\\Apache Software Foundation\\Tomcat 7.0\\webapps\\backup"
                            Del * /a /s /q /f
                        """)
                except:
                    trace=traceback.format_exc()
                    print(trace)
                sleep(1)
            elif operation=="Stop":
                stop(name_service)
            elif operation=="Start":
                start(name_service)
            elif operation=="Deploy_axis":
                stop(name_service)
                sleep(1)
                deploy_axis(directoryStubAar, nameStubAar)
                start(name_service)
            elif operation=="Deploy_axis2":
                stop(name_service)
                sleep(1)
                deploy_axis(sec_dir, nameStubAar)
                start(name_service)
            elif operation=="GetLog":
                try:
                    if is_unix():
                        shell(f"""
                            cd /opt/Tomcat\\ 7.0/logs
                            mkdir /mnt/Log_Tomcat/{it}
                            cp /opt/Tomcat\\ 7.0/logs/* /mnt/Log_Tomcat/{it}
                        """)
                    else:
                        shell(f"""
                            cd /d "C:\\Program Files\\Apache Software Foundation\\Tomcat 7.0\\logs"
                            mkdir {directoryLog}\\{it}
                            robocopy /e . {directoryLog}\\{it}
                        """)
                except:
                    trace=traceback.format_exc()
                    print(trace)
