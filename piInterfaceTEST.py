'''This script establishes ssh connections from the control device to the Pis on the Roombas. Written by Cael Shoop.'''

import paramiko

# Create SSH connection to both Pis/Roombas
def Connect():
    print('Creating SSH connections to Pi0 and Pi1...')

    ip0 = '192.168.1.4'
    pi0User = 'pi'
    pi0Pw = 'ModelIoT'
    port0 = '/dev/ttyUSB0'

    ip1 = '192.168.1.36'
    pi1User = 'pi'
    pi1Pw = 'ModelIoT'
    port1 = '/dev/ttyUSB0'

    ssh0 = paramiko.SSHClient()
    ssh1 = paramiko.SSHClient()

    global ssh
    ssh = []

    try:
        print('Preparing SSH connections...')
        ssh0.load_system_host_keys()
        ssh1.load_system_host_keys()
        print('Success.')
    except:
        print('Failed to set up SSH. Exiting.')
        exit()

    try:
        print('Establishing SSH connection to Pi0...')
        ssh0.connect(ip0, username=pi0User, password=pi0Pw, look_for_keys=False)
        stdin, stdout, stderr = ssh0.exec_command('echo "Hello world!"')
        if stdin or stdout or stderr == 'Hello world!':
            print('Success.')
        ssh.append(ssh0)
    except:
        print('Connection to Pi0 Failed.')

    try:
        print('Establishing SSH connection to Pi1...')
        ssh1.connect(ip1, username=pi1User, password=pi1Pw, look_for_keys=False)
        stdin, stdout, stderr = ssh1.exec_command('echo "Hello world!"')
        if stdin or stdout or stderr == 'Hello world!':
            print('Success.')
        ssh.append(ssh1)
    except:
        print('Connection to Pi1 Failed.')

    return ssh

# Send parameter commands to a Pi/Roomba
def Send(com, piNum):
    try:
        print(f'Sending command \'{com}\' to Pi{piNum}...')
        ssh[piNum].exec_command(com)
        print(f'Command sent to Pi{piNum}.')
    except:
        print(f'Command failed to send to Pi{piNum}.')

# Send file to both Pis
def Transfer(localpath, remotepath):
    if ssh[0]:
        print(f'Sending {localpath} to Pi0...')
        try:
            sftp0 = ssh[0].open_sftp()
            sftp0.put(localpath, remotepath)
            sftp0.close()
            print('Success.')
        except:
            print(f'Failed to send {localpath} to Pi0.')
    if ssh[1]:
        print(f'Sending {localpath} to Pi1...')
        try:
            sftp1 = ssh[1].open_sftp()
            sftp1.put(localpath, remotepath)
            sftp1.close()
            print('Success.')
        except:
            print(f'Failed to send {localpath} to Pi1.')

# Test function to test connection to Pis/Roombas
def Test():
    print('Running roombaTest.py on both devices...')
    ssh[0].exec_command('cd Roomba/IoTdevices')
    ssh[1].exec_command('cd Roomba/IoTdevices')
    time.sleep(1)
    ssh[0].exec_command('python3 roombaTest.py')
    ssh[1].exec_command('python3 roombaTest.py')
    time.sleep(10)
    ssh[0].exec_command('cd ~')
    ssh[1].exec_command('cd ~')
    print('roombaTest.py complete.')

# Close SSH connections
def Disconnect():
    try:
        print('Closing Pi0 SSH connection...')
        ssh[0].close()
        print('Success.')
    except:
        print('Pi0 SSH connection already closed.')

    try:
        print('Closing Pi1 SSH connection...')
        ssh[1].close()
        print('Success.')
    except:
        print('Pi1 SSH connection already closed.')