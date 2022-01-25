'''Test File for moving Roombas. Written by Cael Shoop.'''

from pycreate2 import Create2
import time


port = '/dev/ttyUSB0' # ttyUSB0
print('Port set to \'/dev/ttyUSB0\'.')
roomba = Create2(port)
print('Roomba object created.')
roomba.start()
print('Roomba OI started.')
roomba.safe()
print('Roomba set to safe mode.')
roomba.drive_direct(-200, -200)
print('Roomba told to move backwards at 40% speed for 2 seconds.')
time.sleep(2)
roomba.drive_stop()
print('Roomba told to stop.')
roomba.drive_direct(-200, 200)
print('Roomba told to rotate clockwise at 40% speed for 2 seconds.')
time.sleep(2)
roomba.drive_stop()
print('Roomba told to stop.')
roomba.close()
print('Roomba OI closed.')