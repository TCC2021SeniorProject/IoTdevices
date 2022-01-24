'''Test File for moving Roombas. Written by Cael Shoop.'''

from pycreate2 import Create2
import time


port = '/dev/ttyUSB0' # ttyUSB0
print('Port set to \'/dev/ttyS0\'')
roomba = Create2(port)
print('Roomba object created')
roomba.start()
print('Roomba OI started')
roomba.safe()
print('Roomba set to safe mode')
try:
    sensors = roomba.get_sensors()
    if sensors:
        print('Got Roomba info')
        print(sensors.battery_charge())
except:
    print('Unable to retrieve Roomba data.')
roomba.drive_direct(-200, -200)
time.sleep(2)
roomba.drive_stop()
roomba.drive_direct(-100, 100)
time.sleep(5)
roomba.drive_stop()
roomba.close()