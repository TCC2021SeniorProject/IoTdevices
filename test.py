from pycreate2 import Create2
import time

roomba = Create2('/dev/ttyUSB1')
print('Setting to start')
roomba.start()
print('Setting to full')
roomba.full()
print('Drive backwards (2s)')
roomba.drive_direct(-200, -200)
time.sleep(2)
print('Stop')
roomba.drive_stop()
print('Dock (5s)')
roomba.seek_dock()
time.sleep(5)
print('Disconnect')
roomba.close()
