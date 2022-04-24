'''This script establishes ssh connections from the control device to the Pis on the Roombas. Written by Cael Shoop.'''
# With some modifications it could be used with different devices that accept ssh connections as well.

import paramiko
import time

# Create SSH connection to both Pis/Roombas
def Connect():
    print('Creating SSH connections to Pi0 and Pi1...')

    ip0 = '192.168.0.5'
    pi0User = 'pi'
    pi0Pw = 'ModelIoT'
    port0 = '/dev/ttyUSB0'

    ip1 = '192.168.0.6'
    pi1User = 'pi'
    pi1Pw = 'ModelIoT'
    port1 = '/dev/ttyUSB0'

    ssh0 = paramiko.SSHClient()
    ssh1 = paramiko.SSHClient()

    global initialized
    global ssh
    global channel
    initialized = []
    initialized.append(False)
    initialized.append(False)
    ssh = []
    channel = []

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
        ssh.append(ssh0)
        channel0 = ssh0.invoke_shell()
        channel.append(channel0)
        print('Success.')
    except:
        print('Connection to Pi0 Failed.')
        exit()

    try:
        print('Establishing SSH connection to Pi1...')
        ssh1.connect(ip1, username=pi1User, password=pi1Pw, look_for_keys=False)
        ssh.append(ssh1)
        channel1 = ssh1.invoke_shell()
        channel.append(channel1)
        print('Success.')
    except:
        print('Connection to Pi1 Failed.')
        exit()

# Send parameter commands to a Pi/Roomba
def Send(com, piNum):
    try:
        print(f'Sending command \'{com}\' to Pi{piNum}...')
        ssh[piNum].exec_command(com)
        print(f'Command sent to Pi{piNum}.')
    except:
        print(f'Command failed to send to Pi{piNum}.')

# Send parameter commands to a Pi/Roomba
def SendBoth(com):
    try:
        print(f'Sending command \'{com}\' to Pi0...')
        ssh[0].exec_command(com)
        print(f'Command sent to Pi0.')
    except:
        print(f'Command failed to send to Pi0.')
    try:
        print(f'Sending command \'{com}\' to Pi1...')
        ssh[1].exec_command(com)
        print(f'Command sent to Pi1.')
    except:
        print(f'Command failed to send to Pi1.')

# Sends messages in shell
def Shell(com, piNum):
    if len(com) > 0 and com[-1] != '\n':
        com = com + '\n'
    if not initialized[piNum]:
        out = channel[piNum].recv(9999)
        initialized[piNum] = True
    channel[piNum].send(com)
    while not channel[piNum].recv_ready():
        time.sleep(.1)
    out = channel[piNum].recv(9999)
    output = out.decode("ascii")
    return output

# Sends a message to both shells
def ShellBoth(com):
    if len(com) > 0 and com[-1] != '\n':
        com = com + '\n'
    if not initialized[0]:
        out0 = channel[0].recv(9999)
        initialized[0] = True
    channel[0].send(com)
    while not channel[0].recv_ready():
        time.sleep(.1)
    out0 = channel[0].recv(9999)

    if not initialized[1]:
        out1 = channel[1].recv(9999)
        initialized[1] = True
    channel[1].send(com)
    while not channel[1].recv_ready():
        time.sleep(.1)
    out1 = channel[1].recv(9999)

    return out0.decode("ascii"), out1.decode("ascii")

# Check if a Pi has a file
def Check(localpath, piNum):
    localpath = str(localpath)
    if not initialized[piNum]:
        out = channel[piNum].recv(9999)
        initialized[piNum] = True
    channel[piNum].send('ls | grep ' + localpath + '\n')
    while not channel[piNum].recv_ready():
        time.sleep(.1)
    out = channel[piNum].recv(9999)
    results = out.decode("ascii").split('\n')
    results = results[1:]
    if localpath in results:
        return True
    else:
        return False

# Check if a file is on both Pis
def CheckBoth(localpath):
    localpath = str(localpath)
    if not initialized[0]:
        out0 = channel[0].recv(9999)
        initialized[0] = True
    channel[0].send('ls | grep ' + localpath + '\n')
    while not channel[0].recv_ready():
        time.sleep(.1)
    out0 = channel[0].recv(9999)
    results0 = out0.decode("ascii").split('\n')

    if not initialized[1]:
        out1 = channel[1].recv(9999)
        initialized[1] = True
    channel[1].send('ls | grep ' + localpath + '\n')
    while not channel[1].recv_ready():
        time.sleep(.1)
    out1 = channel[1].recv(9999)
    results1 = out1.decode("ascii").split('\n')

    if localpath in results0[1:] and localpath in results1[1:]:
        return True
    else:
        return False

# Retrieve a file from one Pi
def Retrieve(remotepath, piNum):
    localpath = remotepath[:-4] + str(piNum) + remotepath[-4:]
    try:
        sftp = ssh[piNum].open_sftp()
        sftp.get(remotepath, localpath)
        sftp.close()
        print(f'{remotepath} retrieved successfully from Pi{piNum}.')
    except:
        print(f'File retrieval failed from Pi{piNum}.')

# Retrieve a file from both Pis
def RetrieveBoth(remotepath):
    localpath0 = remotepath[:-4] + '0' + remotepath[-4:]
    localpath1 = remotepath[:-4] + '1' + remotepath[-4:]
    try:
        sftp0 = ssh[0].open_sftp()
        sftp0.get(remotepath, localpath0)
        sftp0.close()
        print(f'{localpath0} successfully retrieved from Pi0.')
    except:
        print(f'File retrieval failed from Pi0.')
    try:
        sftp1 = ssh[1].open_sftp()
        sftp1.get(remotepath, localpath1)
        sftp1.close()
        print(f'{localpath1} successfully retrieved from Pi1.')
    except:
        print(f'File retrieval failed from Pi1.')

# Send file to one Pi
def Transfer(localpath, piNum):
    remotepath = localpath
    try:
        print(f'Sending {localpath} to Pi{piNum}.')
        sftp = ssh[piNum].open_sftp()
        sftp.put(localpath, remotepath)
        sftp.close()
        print('Success.')
    except:
        print(f'Failed to send {localpath} to Pi{piNum}.')

# Send file to both Pis
def TransferBoth(localpath):
    remotepath = localpath
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