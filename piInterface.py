'''Script to run on main device. Written by Cael Shoop.'''
# This script establishes ssh connections from the control device to the Pis on the Roombas.

import paramiko

# Create SSH connection to both Pis
def piConnect():
    print('Creating SSH connections to Pi0 and Pi1...')
    ip0 = '192.168.1.4'
    pi0User = 'pi'
    pi0Pw = 'ModelIoT'
    ip1 = '192.168.1.36'
    pi1User = 'pi'
    pi1Pw = 'ModelIoT'

    print('Creating SSH objects for Pi0...')
    ssh0 = paramiko.SSHClient()
    print('Creating SSH objects for Pi1...')
    ssh1 = paramiko.SSHClient()
    print('Loading system host keys for Pi0...')
    ssh0.load_system_host_keys()
    print('Loading system host keys for Pi1...')
    ssh1.load_system_host_keys()
    print('Setting missing host key policy for Pi0...')
    ssh0.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print('Setting missing host key policy for Pi1...')
    ssh1.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        print('Establishing SSH connection to Pi0...')
        ssh0.connect(ip0, username=pi0User, password=pi0Pw, look_for_keys=False)
        print('Pi0 SSH connection established.\nMoving to IoTdevices directory...')
        ssh0.exec_command('~/cd Roomba/IoTdevices')
        print('Pi0 SSH is now in IoTdevices directory.')
    except:
        print('Connection to Pi0 Failed.')

    try:
        print('Establishing SSH connection to Pi0...')
        ssh1.connect(ip1, username=pi1User, password=pi1Pw, look_for_keys=False)
        print('Pi1 SSH connection established.\nMoving to IoTdevices directory...')
        ssh1.exec_command('~/cd Roomba/IoTdevices')
        print('Pi1 SSH is now in IoTdevices directory.')
    except:
        print('Connection to Pi1 Failed.')

    return ssh0, ssh1

# Send parameter commands to Pis
def piSend(ssh0, ssh1, com):
    try:
        print(f'Sending command \'{com}\' to Pi0...')
        ssh0.exec_command(com)
        print('Command sent to Pi0.')
    except:
        print('Command failed to send to Pi0.')

    try:
        print(f'Sending command \'{com}\' to Pi1...')
        ssh1.exec_command(com)
        print('Command sent to Pi1.')
    except:
        print('Command failed to send to Pi1.')


# Test function to test connection to Roombas
def piTest(ssh0, ssh1):
    if ssh0:
        print('Running roombaTest.py on Pi0...')
        ssh0_stdin, ssh0_stdout, ssh0_stderr = ssh0.exec_command('python3 roombaTest.py')
    if ssh1:
        print('Running roombaTest.py on Pi1...')
        ssh1_stdin, ssh1_stdout, ssh1_stderr = ssh1.exec_command('python3 roombaTest.py')
    
    if ssh0:
        print('Pi0 output:')
        output0 = ssh0_stdout.readlines()
        for line in output0:
            print(line)

    if ssh1:
        print('Pi1 output:')
        output1 = ssh1_stdout.readlines()
        for line in output1:
            print(line)

# Close SSH connections
def piDisconnect(ssh0, ssh1):
    try:
        print('Closing Pi0 SSH connection...')
        ssh0.close()
        print('Successfully closed Pi0 SSH connection.')
    except:
        print('Pi0 SSH connection already closed.')

    try:
        print('Closing Pi1 SSH connection...')
        ssh1.close()
        print('Successfully closed Pi1 SSH connection.')
    except:
        print('Pi1 SSH connection already closed.')