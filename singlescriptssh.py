'''This script establishes ssh connections from the control device to the Pis on the Roombas. Written by Cael Shoop.'''

import time
import paramiko

# Create SSH connection to both Pis/Roombas
print('Creating SSH connections to Pi0 and Pi1...')
ip0 = '192.168.1.4'
pi0User = 'pi'
pi0Pw = 'ModelIoT'
port0 = '/dev/ttyUSB0'
ip1 = '192.168.1.36'
pi1User = 'pi'
pi1Pw = 'ModelIoT'
port1 = '/dev/ttyUSB0'

print('Creating SSH object for Pi0...')
ssh0 = paramiko.SSHClient()
print('Success.\nCreating SSH object for Pi1...')
ssh1 = paramiko.SSHClient()
print('Success.\nLoading system host keys for Pi0...')
ssh0.load_system_host_keys()
print('Success.\nLoading system host keys for Pi1...')
ssh1.load_system_host_keys()
print('Success.\nSetting missing host key policy for Pi0...')
ssh0.set_missing_host_key_policy(paramiko.AutoAddPolicy())
print('Success.\nSetting missing host key policy for Pi1...')
ssh1.set_missing_host_key_policy(paramiko.AutoAddPolicy())
print('Success.')

try:
    print('Establishing SSH connection to Pi0...')
    ssh0.connect(ip0, username=pi0User, password=pi0Pw, look_for_keys=False)
    print('Success.\nMoving to IoTdevices directory...')
    ssh0.exec_command('~/cd Roomba/IoTdevices')
    print('Success.\nOpening Python shell...')
    ssh0.exec_command('python3 -i')
    print('Success.\nImporting pycreate2...')
    ssh0.exec_command('from pycreate2 import Create2')
    print('Success.\nCreating Roomba object...')
    ssh0.exec_command('roomba = Create2(\'' + port0 + '\')')
    print('Success.\nStarting Roomba0 OI...')
    ssh0.exec_command('roomba.start()')
    print('Success.\nRoomba0 is ready for commands.')
except:
    print('Connection to Pi0 Failed.')

try:
    print('Establishing SSH connection to Pi1...')
    ssh1.connect(ip1, username=pi1User, password=pi1Pw, look_for_keys=False)
    print('Success.\nMoving to IoTdevices directory...')
    ssh1.exec_command('~/cd Roomba/IoTdevices')
    print('Success.\nOpening Python shell...')
    ssh1.exec_command('python3 -i')
    print('Success.\nImporting pycreate2...')
    ssh1.exec_command('from pycreate2 import Create2')
    print('Success.\nCreating Roomba object...')
    ssh1.exec_command('roomba = Create2(\'' + port1 + '\')')
    print('Success.\nStarting Roomba1 OI...')
    ssh1.exec_command('roomba.start()')
    print('Success.\nRoomba1 is ready for commands.')
except:
    print('Connection to Pi1 Failed.')


try:
    print(f'Sending command to Pi0...')
    ssh0.exec_command('roomba.drive_direct(-200, -200)')
    print(f'Command sent to Pi0.')
except:
    print(f'Command failed to send to Pi0.')

try:
    print(f'Sending command to Pi1...')
    ssh1.exec_command('roomba.drive_direct(-200, -200)')
    print(f'Command sent to Pi1.')
except:
    print(f'Command failed to send to Pi1.')

time.sleep(3)

try:
    print(f'Sending command to Pi0...')
    ssh0.exec_command('roomba.drive_stop()')
    print(f'Command sent to Pi0.')
except:
    print(f'Command failed to send to Pi0.')

try:
    print(f'Sending command to Pi1...')
    ssh1.exec_command('roomba.drive_stop()')
    print(f'Command sent to Pi1.')
except:
    print(f'Command failed to send to Pi1.')

# Test function to test connection to Pis/Roombas
def piTest(ssh0, ssh1):
    print('Running roombaTest.py on both devices...')
    ssh0.exec_command('roomba.close()')
    ssh1.exec_command('roomba.close()')
    ssh0.exec_command('quit()')
    ssh1.exec_command('quit()')
    ssh0_stdin, ssh0_stdout, ssh0_stderr = ssh0.exec_command('python3 roombaTest.py')
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
        ssh0.exec_command('roomba.close()')
        ssh0.exec_command('quit()')
        ssh0.close()
        print('Successfully closed Pi0 SSH connection.')
    except:
        print('Pi0 SSH connection already closed.')

    try:
        print('Closing Pi1 SSH connection...')
        ssh0.exec_command('roomba.close()')
        ssh0.exec_command('quit()')
        ssh1.close()
        print('Successfully closed Pi1 SSH connection.')
    except:
        print('Pi1 SSH connection already closed.')