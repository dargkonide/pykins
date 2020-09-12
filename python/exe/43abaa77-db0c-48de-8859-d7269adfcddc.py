from time import sleep


node('tvsi-erib0054',vars(),data,run_id,job_name,'''
with node('tvsi-erib0054'):
    with node('tvsi-erib0054'):
        with node('tvsi-erib0054'):
            with node('tvsi-erib0054'):
                with node('tvsi-erib0054'):
                    with node('tvsi-erib0054'):
                        print(a)''')
