import time
from pycreate2 import Create2
from os.path import exists

def init():
    global bot
    try:
        bot = Create2('/dev/ttyUSB0')
    except:
        bot = Create2('/dev/ttyUSB1')
    bot.start()
    bot.safe()


def dancing():
    bot.drive_direct(-190, -190)
    time.sleep(1)
    for ii in range(4):
        bot.drive_direct(-450, 450)
        time.sleep(1)
        bot.drive_direct(190, 190)
        time.sleep(1)
    bot.drive_stop()


def seekdock():
    bot.seek_dock()


def finish():
    bot.close()


init()
print('Done.')
input()
dancing()
print('Done.')
input()
seekdock()
print('Done.')
input()
finish()
print('Done.')