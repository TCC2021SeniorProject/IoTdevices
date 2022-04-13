from pycreate2 import Create2
import time

try:
    roomba = Create2('/dev/ttyUSB0')
except:
    roomba = Create2('/dev/ttyUSB1')
print('Setting to start')
roomba.start()
print('Setting to safe')
roomba.safe()
print('Docking')
roomba.seek_dock()
time.sleep(5)
print('Disconnect')
roomba.close()
