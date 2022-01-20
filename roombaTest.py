'''Test File for moving Roombas. Written by Cael Shoop.'''

from pycreate2 import Create2
import time


port = '/dev/ttyS0' # ttyUSB0
roomba = Create2(port)
roomba.start()
roomba.safe()
sensors = roomba.get_sensors()
print(sensors.battery_charge())
if sensors.battery_charge() > 30000:
    roomba.drive_direct(100, 100)
    sleep(10)
    roomba.drive_stop()
roomba.close()