'''Script to run on Main device, written by Cael Shoop.'''
# This script establishes ssh connections to the Pis on the Roombas.

import paramiko


def piConnect(piID):
    if piID == 0:
        print('<<< FEATURE IN PROGRESS >>>')
        ip = '192.168.1.4'
        piUsername = 'pi'
        piPassword = 'ModelIoT'
        ssh = paramiko.SSHClient()

        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, username=piUsername, password=piPassword, look_for_keys=False)

        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('cd Roomba/IoTdevices && python3 roombaDirect.py -d forward -t 10')
        output = ssh_stdout.readlines()
        for line in output:
            print(line)

        return ssh

    elif piID == 1:
        #ssh into Pi1
        print('<<< FEATURE PENDING >>>')
        ip = '192.168.1.36'
        piUsername = 'pi'
        piPassword = 'ModelIoT'

    else:
        print('Invalid Roomba ID. Exiting.')
        exit()


def piDisconnect(ssh):
    ssh.close()