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


def rotate(angle):
    if angle > 0:
        bot.drive_direct(-150, 150)
    elif angle == 0:
        bot.drive_direct(0, 0)
    else:
        angle = -angle
        bot.drive_direct(150, -150)
    time.sleep(angle/69)
    bot.drive_stop()


def disconnect():
    bot.close()


connect()
print('connected')

command = ''
while 'disconnect' not in command:
    prev_com = command

    if 'move' in command:
        dist = float(command[5:])
        move(dist)
        print('moved ' + command[5:])
    
    elif 'rotate' in command:
        ang = float(command[7:])
        rotate(ang)
        print('rotated ' + command[7:])

    command = str(input())

disconnect()
print('disconnected')
