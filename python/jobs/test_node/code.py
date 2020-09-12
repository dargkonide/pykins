service="""[Unit]
Description=Pykins
After=network.target

[Service]
User=root
WorkingDirectory=/opt/data/pykins/python
ExecStart=/usr/bin/python3 /opt/data/pykins/python/core.py

Restart=on-failure

[Install]
WantedBy=multi-user.target
"""

for n in range(4,30):
    with node('tvli-erib07%02d'%n):
        from os import popen

        output=popen(f"""
            sudo mkdir /opt/data/pykins
            sudo cp /home/eriblt/install.sh /opt/data/pykins
            sudo cp -R /home/eriblt/python /opt/data/pykins
        """).read()
        print(output)

        with open('/etc/systemd/system/pykins.service','w') as f:
            f.write(service)
        output=popen(f"""
            sudo systemctl daemon-reload
            sudo systemctl enable pykins
        """).read()
        print(output)