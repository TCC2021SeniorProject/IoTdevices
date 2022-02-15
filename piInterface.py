'''This script establishes ssh connections from the control device to the Pis on the Roombas. Written by Cael Shoop.'''

import paramiko

# Create SSH connection to both Pis/Roombas
def piCon():
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

    ssh = []

    # try:
    #     print('Preparing SSH connections...')
    #     ssh0.load_system_host_keys()
    #     ssh1.load_system_host_keys()
    #     ssh0.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    #     ssh1.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    #     print('Success.')
    # except:
    #     print('Failed to set up SSH. Exiting.')
    #     exit()

    try:
        print('Establishing SSH connection to Pi0...')
        ssh0.connect(ip0, username=pi0User, password=pi0Pw, look_for_keys=False)
        stdin, stdout, stderr = ssh0.exec_command('echo "Hello world!"')
        if stdout == 'Hello world!':
            print('Success.\nRoomba0 is ready for commands.')
        ssh.append(ssh0)
    except:
        print('Connection to Pi0 Failed.')

    try:
        print('Establishing SSH connection to Pi1...')
        ssh1.connect(ip1, username=pi1User, password=pi1Pw, look_for_keys=False)
        stdin, stdout, stderr = ssh1.exec_command('echo "Hello world!"')
        if stdout == 'Hello world!':
            print('Success.\nRoomba1 is ready for commands.')
        ssh.append(ssh1)
    except:
        print('Connection to Pi1 Failed.')

    return ssh

# Send parameter commands to a Pi/Roomba
def piSend(ssh, com, piNum):
    try:
        print(f'Sending command \'{com}\' to Pi{piNum}...')
        ssh.exec_command(com)
        print(f'Command sent to Pi{piNum}.')
    except:
        print(f'Command failed to send to Pi{piNum}.')

# Test function to test connection to Pis/Roombas
def piTest(ssh0, ssh1):
    print('Running roombaTest.py on both devices...')
    ssh0.exec_command('cd Roomba/IoTdevices')
    ssh1.exec_command('cd Roomba/IoTdevices')
    time.sleep(1)
    ssh0.exec_command('python3 roombaTest.py')
    ssh1.exec_command('python3 roombaTest.py')
    time.sleep(10)
    ssh0.exec_command('cd ~')
    ssh1.exec_command('cd ~')
    print('roombaTest.py complete.')

# Close SSH connections
def piDiscon(ssh0, ssh1):
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