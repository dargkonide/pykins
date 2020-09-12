from socket import gethostbyname
from requests import get
from datetime import datetime
from exe.mysql import *
generators_list = ['tvli-erib0720']
if nt == 'NT1':
    for generator in generators_list:
        with node(generator):
            from os import popen
            output=popen(f"""
                sudo mkdir -p /opt/data/FilesForStubs
                cd /opt/data/FilesForStubs
                sudo if [-fe CardToCardResponse.txt]
                then
                rm  CardToCardResponse.txt
            """).read()
            print(output)

