'''Test File for moving Roombas. Written by Cael Shoop.'''

from pycreate2 import Create2
import time


port = '/dev/ttyS0' # ttyUSB0
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
except:
    print('Unable to retrieve Roomba data.')
print(sensors.battery_charge())
if sensors.battery_charge() > 30000:
    roomba.drive_direct(-200, -200)
    sleep(2)
    roomba.drive_stop()
    roomba.drive_direct(-500, 500)
    sleep(3)
    roomba.drive_stop()
roomba.close()