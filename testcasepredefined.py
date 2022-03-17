# Written by Cael Shoop.

def Dock():
    code

def GoFront():
    code

def Ready():
    code

def Connect():
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
        if stdin or stdout or stderr == 'Hello world!\n':
            print('Success.\nRoomba0 is ready for commands.')
        ssh.append(ssh0)
    except:
        print('Connection to Pi0 Failed.')

    try:
        print('Establishing SSH connection to Pi1...')
        ssh1.connect(ip1, username=pi1User, password=pi1Pw, look_for_keys=False)
        stdin, stdout, stderr = ssh1.exec_command('echo "Hello world!"')
        if stdin or stdout or stderr == 'Hello world!\n':
            print('Success.\nRoomba1 is ready for commands.')
        ssh.append(ssh1)
    except:
        print('Connection to Pi1 Failed.')