'''Test File for moving Roombas. Written by Cael Shoop.'''

from pycreate2 import Create2
import time


port = '/dev/ttyS0' # ttyUSB0
roomba = Create2(port)
roomba.start()
roomba.safe()
#roomba.drive_direct(100, 100)
#roomba.drive_stop()
sensors = roomba.get_sensors()
print(sensors.battery_charge())
roomba.close()