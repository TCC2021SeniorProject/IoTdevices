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


def undock():
    bot.drive_direct(-500, -500)
    time.sleep(1)
    bot.drive_stop()


def scan():
    try:
        Obj = PyLidar3.YdLidarX4('/dev/ttyUSB1', chunk_size=6000)
    except:
        Obj = PyLidar3.YdLidarX4('/dev/ttyUSB0', chunk_size=6000)
    if Obj.Connect():
        gen = Obj.StartScanning()
    try:
        Obj.Disconnect()
    except:
        pass


def move(distance):
    if distance > 0:
        bot.drive_direct(225, 225)
    elif distance < 0:
        distance = -distance
        bot.drive_direct(-255, -255)
    else:
        bot.drive_direct(0, 0)
    time.sleep(distance * 3)
    bot.drive_stop()


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
while 'disconnect' not in command:
    prev_com = command

    if 'undock' in command:
        undock()
        print('undocked')

    elif 'scan' in command:
        scan()
        print('scanned')

    elif 'move' in command:
        dist = float(command[5:])
        move(dist)
        print('moved ' + command[5:])
    
    elif 'rotate' in command:
        ang = float(command[7:])
        rotate(ang)
        print('rotated ' + command[7:])

    elif 'dock' in command:
        dock()
        print('docked')

    command = str(input())

disconnect()
print('disconnected')