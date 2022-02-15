'''Script to test piInterface.py. Written by Cael Shoop.'''

import paramiko
import piInterface as piI
import time


ssh = piI.piCon()
time.sleep(1)
if not ssh:
    print('Error. Exiting.')
    exit()
piI.piSend(ssh[0], 'python3 transOut.py', 0)
piI.piSend(ssh[1], 'python3 transOut.py', 1)
time.sleep(3)
piI.piDiscon(ssh[0], ssh[1])