'''Script to test piInterface.py. Written by Cael Shoop.'''

import paramiko
import piInterfaceTEST as piI
import time


ssh = piI.Connect()
time.sleep(1)
if not ssh:
    print('Error. Exiting.')
    exit()

'''This will transfer the file specified and run it'''
piI.Transfer('test.py', 'test.py')
piI.SendBoth('python3 test.py')
time.sleep(5)
piI.SendBoth('rm test.py')
# piI.Transfer('testcasepredefined.py', 'testcasepredefined.py')
# piI.Transfer('output.py', 'output.py')
# piI.SendBoth('python3 output.py')
# piI.SendBoth('rm output.py')

'''Executes written script directly'''
# piI.Send('python3 -c "from pycreate2 import Create2;roomba = Create2("/dev/ttyUSB1");roomba.start();roomba.safe();roomba.drive_direct(-200, -200);time.sleep(2);roomba.drive_stop();time.sleep(1);roomba.seek_dock();roomba.close();quit()\n"', 0)

time.sleep(3)
piI.Disconnect()