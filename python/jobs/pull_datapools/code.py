with node('tvli-erib0703'):

    # Выгрузка датапулов
    if datapools:
        shell(f"""
            cd /opt/data/var/git/{stend}/Datapools
            git reset --hard
            git clean -xfd
            git pull -f 
            git checkout "{branchDatapools}"
            git pull origin "{branchDatapools}"
            chmod -R 777 *
            chown -R root:root *
        """)

    # Выгрузка скриптов
    if ltscripts:
        shell(f"""
            cd /opt/data/var/git/{stend}/ERIB_LTScripts
            git reset --hard
            git clean -xfd
            git pull -f 
            git checkout "{branchLTScripts}"
            git pull -f origin "{branchLTScripts}"
            chmod -R 777 *
            chown -R root:root *
        """)
    
    if stend=='NT2':
        shell(f"sed -i 's/8088/8188/g' /opt/data/var/git/NT2/Datapools/NT2/Influx/InfluxAuth.txt")
