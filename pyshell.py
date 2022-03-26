'''Script to test piInterface.py. Written by Cael Shoop.'''

import paramiko
import piInterface as piI
import time


ssh = piI.Connect()
time.sleep(1)
if not ssh:
    print('Error. Exiting.')
    exit()

'''This will transfer a file to both roombas and run it'''
#Test
piI.Transfer('test.py', 'test.py')
piI.SendBoth('python3 test.py')
time.sleep(10)
piI.SendBoth('rm test.py')
# piI.Transfer('predefined.py', 'predefined.py')
# piI.Transfer('output.py', 'output.py')
# piI.SendBoth('python3 output.py')
# time.sleep(10)
# piI.SendBoth('rm predefined.py')
# piI.SendBoth('rm output.py')

'''This will send a file to one roomba'''
piI.Transfer('predefined.py', 'predefined.py')
piI.Transfer('output.py', 'output.py')
piI.Send('python3 output.py', 0)
time.sleep(10)
piI.Send('rm predefined.py', 0)
piI.Send('rm output.py', 0)

time.sleep(3)
piI.Disconnect()