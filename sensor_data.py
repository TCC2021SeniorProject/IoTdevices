from pycreate2 import Create2
import argparse


try:
    roomba = Create2('/dev/ttyUSB0')
except:
    roomba = Create2('/dev/ttyUSB1')
sensors = roomba.get_sensors()

if sensors:
    parser = argparse.ArgumentParser()
    parser.add_argument('function')
    args = parser.parse_args()
    out = null
    func = 'out = sensors.' + str(args.function) + '()'
    exec(func)
    print(out)