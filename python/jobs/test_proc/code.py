from time import sleep
from socket import gethostname

host=gethostname()

with node(host):
    with node(host):
        with node(host):
            with node(host):
                with node(host):
                    with node(host):
                        with node(host):
                            print(a)