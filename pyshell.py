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
# piI.Transfer('test.py', 'test.py')
# piI.Send('python3 test.py', 0)
# piI.Send('python3 test.py', 1)
piI.Transfer('testcasepredefined.py', 'testcasepredefined.py')
piI.Transfer('output.py', 'output.py')
piI.Send('python3 output.py', 0)
piI.Send('python3 output.py', 1)

'''Executes written script directly'''
#Version 1
# piI.Send('python3 -c "from pycreate2 import Create2;roomba = Create2("/dev/ttyUSB1");roomba.start();roomba.safe();roomba.drive_direct(-200, -200);time.sleep(2);roomba.drive_stop();time.sleep(1);roomba.seek_dock();roomba.close();quit()\n"', 0)
#Version 2
# piI.Send('python3 -c "from pycreate2 import Create2\nroomba = Create2("/dev/ttyUSB1")\nroomba.start()\nroomba.safe()\nroomba.drive_direct(-200, -200)\ntime.sleep(2)\nroomba.drive_stop()\ntime.sleep(1)\nroomba.seek_dock()\nroomba.close()\nquit()\n"', 0)

time.sleep(3)
piI.Disconnect()