'''This script establishes ssh connections from the control device to the Pis on the Roombas. Written by Cael Shoop.'''

import paramiko
import time

# Create SSH connection to both Pis/Roombas
def Connect():
    print('Creating SSH connections to Pi0 and Pi1...')

    ip0 = '192.168.0.7'
    pi0User = 'pi'
    pi0Pw = 'ModelIoT'
    port0 = '/dev/ttyUSB0'

    ip1 = '192.168.0.22'
    pi1User = 'pi'
    pi1Pw = 'ModelIoT'
    port1 = '/dev/ttyUSB0'

    ssh0 = paramiko.SSHClient()
    ssh1 = paramiko.SSHClient()

    global ssh
    global channel
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
        #ssh0.exec_command('echo "Hello world!"')
        #print('Success.')
        channel0 = ssh0.invoke_shell()
        channel.append(channel0)
    except:
        print('Connection to Pi0 Failed.')

    try:
        print('Establishing SSH connection to Pi1...')
        ssh1.connect(ip1, username=pi1User, password=pi1Pw, look_for_keys=False)
        ssh.append(ssh1)
        #ssh1.exec_command('echo "Hello world!"')
        #print('Success.')
        channel1 = ssh1.invoke_shell()
        channel.append(channel1)
    except:
        print('Connection to Pi1 Failed.')

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

# Retrieve sensor data from Roombas
def Sensors(arg, piNum): ########### Untested
    out = channel[piNum].recv(9999)
    channel[piNum].send('python3 sensor_data.py ' + arg + '\n')
    while not channel[piNum].recv_ready():
        time.sleep(3)
    out = channel[piNum].recv(9999)
    return out.decode("ascii")

# Sends messages in shell
def Shell(com, piNum):
    out = channel[piNum].recv(9999)
    channel[piNum].send(com)
    while not channel[piNum].recv_ready():
        time.sleep(3)
    out = channel[piNum].recv(9999)
    
    return out.decode("ascii")

# Sends a message to both shells
def ShellBoth(com):
    out = []
    out0 = channel[0].recv(9999)
    channel[0].send('ls | grep ' + localpath + '\n')
    while not channel[0].recv_ready():
        time.sleep(3)
    out0 = channel[0].recv(9999)
    out.append(out0.decode("ascii"))

    out1 = channel[1].recv(9999)
    channel[1].send('ls | grep ' + localpath + '\n')
    while not channel[1].recv_ready():
        time.sleep(3)
    out1 = channel[1].recv(9999)
    out.append(out1.decode("ascii"))

    return out

# Check if a Pi has a file
def Check(localpath, piNum): ########### Untested
    out = channel[piNum].recv(9999)
    channel[piNum].send('ls | grep ' + localpath + '\n')
    while not channel[piNum].recv_ready():
        time.sleep(3)
    out = channel[piNum].recv(9999)
    if localpath in out.decode("ascii"):
        return True
    else:
        return False

# Check if a file is on both Pis
def CheckBoth(localpath): ########### Untested
    out0 = channel[0].recv(9999)
    channel[0].send('ls | grep ' + localpath + '\n')
    while not channel[0].recv_ready():
        time.sleep(3)
    out0 = channel[0].recv(9999)

    out1 = channel[1].recv(9999)
    channel[1].send('ls | grep ' + localpath + '\n')
    while not channel[1].recv_ready():
        time.sleep(3)
    out1 = channel[1].recv(9999)

    if localpath in out0.decode("ascii") and localpath in out1.decode("ascii"):
        return True
    else:
        return False

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