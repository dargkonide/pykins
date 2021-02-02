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


with node(server):
    from os import popen
    with open('/etc/systemd/system/pykins.service','w') as f:
        f.write(service)

    output=popen(f"""
        sudo systemctl daemon-reload
        sudo systemctl enable pykins
    """).read()

    print(output)