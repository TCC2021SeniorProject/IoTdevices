'''This script establishes ssh connections from the control device to the Device s on the Roombas. Written by Cael Shoop.'''
# This version includes untested changes that should allow it to work with any number of devices.

import paramiko
import time
import configparser as cp
import os

# Attempt to create SSH connection to all devices in cfg file
# Can be run by passing in a list of device IPs
def Connect(deviceIPs=[]):
    if len(deviceIPs) == 0:
        print('No devices passed in to connect to. Exiting.')
        exit(-1)
    deviceCfg = cp.ConfigParser()
    if os.path.exists('deviceConfig.ini'):
        deviceCfg.read_file(open('deviceConfig.ini'))
    else:
        print('Error: No config file. Please run DeviceSetup.py.')
        exit(-1)

    global sshs
    global channels
    sshs = []
    channels = []

    try:
        print('Establishing connections...')
        for ip in deviceCfg.sections():
            if ip in deviceIPs:
                ssh = paramiko.SSHClient()
                ssh.load_system_host_keys()
                curUser = None
                curPw = None
                try:
                    ssh.connect(ip, username=curUser, password=curPw, look_for_keys=False)
                    sshs.append(ssh)
                    channel = ssh.invoke_shell()
                    channels.append(channel)
                    print(str(ip) + ' connected.')
                except:
                    print(str(ip) + ' failed to connect.')
            else:
                print(str(ip) + ' not in passed IP list, excluding.')
        if len(sshs) == len(deviceIPs):
            print('Success.')
            global initialized
            initialized = []
            for ii in range(len(sshs)):
                initialized.append(False)
        else:
            print('Failed to connect to the specified number of devices.')
            exit(-1)
        deviceCfg.close()
    except:
        print('Failed to set up SSH. Exiting.')
        exit()

# Send parameter commands to a device
def Send(com, deviceNum):
    try:
        print(f'Sending command \'{com}\' to Device {deviceNum}...')
        sshs[deviceNum].exec_command(com)
        print(f'Command sent to Device {deviceNum}.')
    except:
        print(f'Command failed to send to Device {deviceNum}.')

# Send parameter commands to all devices
def SendAll(com):
    for ii in range(len(sshs)):
        try:
            print(f'Sending command \'{com}\' to Device {ii}...')
            ssh[ii].exec_command(com)
            print(f'Command sent to Device {ii}.')
        except:
            print(f'Command failed to send to Device {ii}.')

# Sends messages in shell
def Shell(com, deviceNum):
    if len(com) > 0 and com[-1] != '\n':
        com = com + '\n'
    if not initialized[deviceNum]:
        out = channel[deviceNum].recv(9999)
        initialized[deviceNum] = True
    channel[deviceNum].send(com)
    while not channel[deviceNum].recv_ready():
        time.sleep(.1)
    out = channel[deviceNum].recv(9999)
    result = out.decode("ascii")
    return result

# Sends a message to all shells, returns list of all outputs
def ShellAll(com):
    if len(com) > 0 and com[-1] != '\n':
        com = com + '\n'
    results = []
    for ii in range(len(sshs)):
        if not initialized[ii]:
            out = channel[ii].recv(9999)
            initialized[ii] = True
        channel[ii].send(com)
        while not channel[ii].recv(9999):
            time.sleep(.1)
        out = channel[ii].recv(9999)
        result = out.decode('ascii')
        results.append(result)
    return results

# Check if a file is on a device
def Check(localpath, deviceNum):
    localpath = str(localpath)
    if not initialized[deviceNum]:
        out = channel[deviceNum].recv(9999)
        initialized[deviceNum] = True
    channel[deviceNum].send('ls | grep ' + localpath + '\n')
    while not channel[deviceNum].recv_ready():
        time.sleep(.1)
    out = channel[deviceNum].recv(9999)
    results = out.decode("ascii").split('\n')
    results = results[1:]
    if localpath in results:
        return True
    else:
        return False

# Check if a file is on all devices
def CheckAll(localpath):
    localpath = str(localpath)
    allResults = []
    onAllDevices = True
    for ii in range(len(sshs)):
        if not initialized[ii]:
            out = channel[ii].recv(9999)
            initialized[ii] = True
        channel[ii].send('ls | grep ' + localpath + '\n')
        while not channel[ii].recv_ready():
            time.sleep(.1)
        out = channel[0].recv(9999)
        results = out.decode('ascii').split('\n')
        if localpath in results[1:]:
            allResults.append(True)
            print(f'{localpath} found on Device {ii}.')
        else:
            onAllDevices = False
            print(f'{localpath} not found on Device {ii}.')
    if onAllDevices == True:
        print(f'{localpath} found on all devices.')
        return True
    else:
        print(f'{localpath} not found on all devices.')
        return False

# Retrieve a file from one Device 
def Retrieve(remotepath, deviceNum):
    localpath = remotepath[:-4] + str(deviceNum) + remotepath[-4:]
    try:
        sftp = sshs[deviceNum].open_sftp()
        sftp.get(remotepath, localpath)
        sftp.close()
        print(f'{localpath} successfully retrieved from Device {deviceNum}.')
    except:
        print(f'File retrieval failed from Device {deviceNum}.')

# Retrieve a file from all devices
def RetrieveAll(remotepath):
    localpaths = []
    for ii in range(len(sshs)):
        localpath = remotepath[:-4] + str(ii) + remotepath[-4:]
        localpaths.append(localpath)
    counter = 0
    for ssh in sshs:
        try:
            sftp = ssh.open_sftp()
            sftp.get(remotepath, localpaths[counter])
            sftp.close()
            print(f'{localpaths[counter]} successfully retrieved from Device {counter}.')
        except:
            print(f'File retrieval failed from Device {counter}.')

# Send file to one device
def Transfer(localpath, deviceNum):
    remotepath = localpath
    try:
        print(f'Sending {localpath} to Device {deviceNum}.')
        sftp = sshs[deviceNum].open_sftp()
        sftp.put(localpath, remotepath)
        sftp.close()
        print('Success.')
    except:
        print(f'Failed to send {localpath} to Device {deviceNum}.')

# Send file to all devices
def TransferAll(localpath):
    remotepath = localpath
    for ssh in sshs:
        print(f'Sending {localpath}...')
        try:
            sftp = ssh.open_sftp()
            sftp.put(localpath, remotepath)
            sftp.close()
            print('Success.')
        except:
            print(f'Failed to send {localpath}.')

# Close all SSH connections
def Disconnect():
    print('Closing connections...')
    for ssh in sshs:
        try:
            ssh.close()
            print('Connection closed successfully.')
        except:
            print('Connection already closed.')