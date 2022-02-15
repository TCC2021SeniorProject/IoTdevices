'''Script to test piInterface.py. Written by Cael Shoop.'''

import paramiko
import piInterface as piI
import time


ssh0, ssh1 = piI.piCon()
time.sleep(1)
piI.piSend(ssh0, 'python3 transOut.py', 0)
piI.piSend(ssh1, 'python3 transOut.py', 1)
time.sleep(3)
piI.piDiscon(ssh0, ssh1)