# Written by Cael Shoop.

import time
from pycreate2 import Create2

def com_dance():
    bot.drive_direct(-190, -190)
    time.sleep(1)
    bot.drive_direct(-450, 450)
    time.sleep(1)
    bot.drive_direct(190, 190)
    time.sleep(1)
    bot.drive_direct(-450, 450)
    time.sleep(1)
    bot.drive_direct(190, 190)
    time.sleep(1)
    bot.drive_direct(-450, 450)
    time.sleep(1)
    bot.drive_direct(190, 190)
    time.sleep(1)
    bot.drive_direct(-450, 450)
    time.sleep(1)
    bot.drive_direct(190, 190)
    time.sleep(1)
    bot.drive_stop()
    done = 1


def com_dock():
    bot.seek_dock()
    time.sleep(2)
    bot.close()


def com_init():
    global bot
    try:
        bot = Create2('/dev/ttyUSB0')
    except:
        bot = Create2('/dev/ttyUSB1')
    bot.start()
    bot.safe()