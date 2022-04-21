import time
from pycreate2 import Create2
import PyLidar3

def connect():
    global bot
    try:
        bot = Create2('/dev/ttyUSB0')
    except:
        bot = Create2('/dev/ttyUSB1')
    bot.start()
    bot.safe()


def rotate(angle):
    if angle > 0:
        if angle > 45:
            bot.drive_direct(-150, 150)
        else:
            bot.drive_direct(-165, 165)
    elif angle == 0:
        bot.drive_direct(0, 0)
    else:
        angle = -angle
        if angle > 45:
            bot.drive_direct(150, -150)
        else:
            bot.drive_direct(165, -165)
    time.sleep(angle/69)
    bot.drive_stop()


def disconnect():
    bot.close()


connect()
print('connected')

command = ''
while 'disconnect' not in command:
    prev_com = command

    if 'rotate' in command:
        ang = float(command[7:])
        rotate(ang)
        print('rotated ' + command[7:])

    command = str(input())

disconnect()
print('disconnected')