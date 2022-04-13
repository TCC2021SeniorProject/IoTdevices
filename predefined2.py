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


# def undock():
#     bot.drive_distance(-.15, 200, True)
#     sensors = bot.get_sensors()
#     while sensors.velocity > 5:
#         time.sleep(.1)
#         sensors = bot.get_sensors()

def undock():
    bot.drive_direct(-200, -200)
    time.sleep(.7)
    bot.drive_stop()

# def move(distance):
#     bot.drive_distance(distance, 300, True)
#     wait = distance * 2
#     if wait < 0:
#         wait = -wait
#     time.sleep(wait)

def move(distance):
    bot.drive_direct(300, 300)
    time.sleep(distance * 2)
    bot.drive_stop()

# def rotate(angle):
#     bot.turn_angle(angle, 350)
#     wait = angle/45
#     if wait < 0:
#         wait = -wait
#     time.sleep(wait)

def rotate(angle):
    if angle > 0:
        bot.drive_direct(150, -150)
    elif angle == 0:
        bot.drive_direct(0, 0)
    else:
        angle = -angle
        bot.drive_direct(-150, 150)
    time.sleep(angle/70)
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