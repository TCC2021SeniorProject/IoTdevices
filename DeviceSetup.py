'''Written by Cael Shoop. This script will make adding new devices to the config file quick and painless.'''

import configparser as cp
import os


deviceCfg = cp.ConfigParser()
if os.path.exists('deviceConfig.ini'):
    deviceCfg.read_file(open('deviceConfig.ini'))
else:
    with open('deviceConfig.ini', 'x') as fp:
        pass
    deviceCfg.read('deviceConfig.ini')
newIP = ''
print('Existing devices:')
for section in deviceCfg.sections():
    print(section)
while '-1' not in newIP:
    newIP = input('Enter new device\'s IP address (-1 to exit): ').strip('\n')
    if deviceCfg.has_section(newIP):
        print('IP already in deviceConfig.ini.')
    elif '-1' not in newIP:
        deviceAdd = cp.ConfigParser()
        deviceAdd.add_section(newIP)
        deviceAdd[newIP] = {}
        newUser = input('Enter the device\'s username: ').strip('\n')
        if '-1' in newUser:
            print('Exiting.')
            exit(-1)
        newPass = input('Enter the device\'s password: ').strip('\n')
        if '-1' in newPass:
            print('Exiting.')
            exit(-1)
        deviceAdd[newIP]['username'] = newUser
        deviceAdd[newIP]['password'] = newPass
        with open('deviceConfig.ini', 'a') as fp:
            deviceAdd.write(fp)
        print(f'Device with IP \'{newIP}\', username \'{newUser}\', and password \'{newPass}\' added.')
    else:
        print('Exiting.')