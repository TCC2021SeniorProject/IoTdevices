'''Script to test piInterface.py. Written by Cael Shoop.'''

import paramiko
import piInterface as piI
import time


ssh0, ssh1 = piI.piConnect()
time.sleep(1)
piI.piSend(ssh0, 'drive_direct(-200, -200)', 0)
piI.piSend(ssh1, 'drive_direct(-200, -200)', 1)
time.sleep(2)
piI.piSend(ssh0, 'drive_direct(-300, 300)', 0)
piI.piSend(ssh1, 'drive_direct(300, -300)', 1)
time.sleep(3)
piI.piDisconnect(ssh0, ssh1)