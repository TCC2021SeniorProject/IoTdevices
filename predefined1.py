'''Written by Cael Shoop to be transfered to the Pis and run remotely.'''

import time
from pycreate2 import Create2


def connect():
    global bot
    try:
        bot = Create2('/dev/ttyUSB0')
    except:
        bot = Create2('/dev/ttyUSB1')
    bot.start()
    bot.safe()


def dance0():
    bot.drive_direct(-190, -190)
    time.sleep(1)
    bot.drive_direct(-420, 420)
    time.sleep(2)
    bot.drive_stop()


def dance1():
    bot.drive_direct(-190, -190)
    time.sleep(1)
    bot.drive_direct(420, -420)
    time.sleep(2)
    bot.drive_stop()


def dock():
    bot.seek_dock()
    sensors0 = bot.get_sensors()
    time.sleep(.3)
    sensors1 = bot.get_sensors()
    time.sleep(.3)
    sensors2 = bot.get_sensors()
    time.sleep(.3)
    while sensors0.charger_state == 0 and sensors1.charger_state == 0 and sensors2.charger_state == 0:
        time.sleep(1)
        sensors0 = bot.get_sensors()
        time.sleep(.3)
        sensors1 = bot.get_sensors()
        time.sleep(.3)
        sensors2 = bot.get_sensors()
        time.sleep(.3)


def disconnect():
    bot.close()


connect()
print('connected')

command = ''
while command != 'disconnect':
    if command == 'dance0':
        dance0()
        print('danced0')

    elif command == 'dance1':
        dance1()
        print('danced1')

    elif command == 'dock':
        dock()
        print('docked')

    command = str(input())

disconnect()
print('disconnected')
