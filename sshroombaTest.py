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

try:
    print('Establishing SSH connection to Pi0...')
    ssh0 = paramiko.SSHClient()
    ssh0.load_system_host_keys()
    ssh0.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh0.connect(ip0, username=pi0User, password=pi0Pw, look_for_keys=False)
    ssh0.exec_command('~/cd Roomba/IoTdevices')
    ssh0.exec_command('git pull')
    print('Success.')
except:
    print('Connection to Pi0 Failed.')

try:
    print('Establishing SSH connection to Pi1...')
    ssh1 = paramiko.SSHClient()
    ssh1.load_system_host_keys()
    ssh1.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh1.connect(ip1, username=pi1User, password=pi1Pw, look_for_keys=False)
    ssh1.exec_command('~/cd Roomba/IoTdevices')
    ssh1.exec_command('git pull')
    print('Success.')
except:
    print('Connection to Pi1 Failed.')

time.sleep(5)

print('Running roombaTest.py on both devices...')
ssh0.exec_command('python3 roombaTest.py')
ssh1.exec_command('python3 roombaTest.py')

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