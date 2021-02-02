with node("tvli-erib0703"):
    # shell('python3 -m pip install pymysql')
    from exe.mysql import *
    import socket
    
    with connect('test') as con:
        for server in servers.split(','):
            server=server.strip()

            #if (it =~ /^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$/){
            try:socket.inet_aton(server)
            except:ip=socket.gethostbyname(server)
            else:ip=server

            dir_pool=f"//{ip}/git"
            print(f"Меняем линк на папку стенда {stend} для ip {ip}")

            # создаём директорию для конкретного IP для создания в ней симлинки
            shell(f"""
                cd /opt/data/var/generators
                if [ ! -d "{ip}" ];  then
                    mkdir {ip}
                    chmod -R 777 {ip}                
                fi
            """)

            # удаляем симлинки, если они есть
            shell(f"""
                cd /opt/data/var/generators/"{ip}"
                if [ -d datafiles ]; then unlink datafiles; fi
                if [ -d ERIBScripts ]; then unlink ERIBScripts; fi
            """)

            if local:
                # Если выбран локальный стенд, сначала смонтируем сетевой раздел с машины, на которой работаем.
                # Для подключения сетевых разделов вшит технологический пользователь
                shell(f"""
                    cd /mnt
                    if [ -d "{ip}/Datapools" ]; then umount -l /mnt/{ip}; fi
                    if [ -d "{ip}" ]; then rm -Rf {ip}; fi
                    mkdir {ip}
                    mount -t cifs {dir_pool} -o vers=1.0,username=eriblt,domain=alpha,password={password} /mnt/{ip}
                """)
                shell(f"""
                    cd /opt/data/var/generators/{ip}		
                    ln -s /mnt/{ip}/Datapools/{stend} datafiles
                    ln -s /mnt/{ip}/ERIB_LTScripts  ERIBScripts
                """)
            else:
                # создаём симлинки на НТ1 или НТ2
                shell(f"""
                    cd /opt/data/var/generators/{ip}			
                    ln -s /opt/data/var/git/{stend}/Datapools/{stend} datafiles
                    ln -s /opt/data/var/git/{stend}/ERIB_LTScripts  ERIBScripts
                """)
                
                insert(con,"update generators_link set stend=%s where generator_ip=%s",[[stend,server]])
