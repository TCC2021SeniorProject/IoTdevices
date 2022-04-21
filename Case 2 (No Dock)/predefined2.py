import time
from pycreate2 import Create2
import PyLidar3
import matplotlib.pyplot as plt
import matplotlib
import math
import statistics

def connect():
    global bot
    try:
        bot = Create2('/dev/ttyUSB0')
    except:
        bot = Create2('/dev/ttyUSB1')
    bot.start()
    bot.safe()


def scanMap():
    port = '/dev/ttyUSB1'
    curScan = []
    allScans = {}
    
    Obj = PyLidar3.YdLidarX4(port, chunk_size=6000)
    if Obj.Connect():
        gen = Obj.StartScanning()
        # Number of scans to be taken
        for i in range(25):
            curScan = next(gen)
            # print(curScan[0])
            for angle in range(0,360):
                # Must be greater than min distance
                if angle not in allScans.keys():
                    allScans.update({angle: [curScan[angle]]})
                else:
                    allScans[angle].append(curScan[angle])
    Obj.Disconnect()
    
    # Process scan data
    meanScan = {}
    stdevScan = {}
    varScan = {}
    
    # Take mean and standard diviation of scans
    for angle in allScans:
        meanScan.update({angle: statistics.mean(allScans.get(angle))})
        varScan.update({angle: statistics.variance(allScans.get(angle))})
        stdevScan.update({angle: statistics.stdev(allScans.get(angle))})
    
    acceptedScan = {}
    
    # Only accepting values within standard diviation
    for angle in allScans:
        for dist in allScans.get(angle):
            if (meanScan.get(angle) - stdevScan.get(angle) > dist < meanScan.get(angle) + stdevScan.get(angle)) and varScan.get(angle) < 2000:
                if angle not in acceptedScan.keys():
                    acceptedScan.update({angle: [dist]})
                else:
                    acceptedScan[angle].append(dist)

    # Take mean of accepted distances
    estimatedMap = {}
    for angle in acceptedScan:
        estimatedMap.update({angle: statistics.mean(acceptedScan.get(angle))})
     
    estimatedMap = acceptedScan
    
    # Map lidar scan & save as image (.png)
    #matplotlib.use("TkAgg")

    fig = plt.figure(1)
    
    fig.canvas.manager.set_window_title("Pi#1")
    axe = fig.add_subplot(111)
    plt.cla()
    
    x = [0 for _ in range(360)]
    y = [0 for _ in range(360)]
    
    for angle in estimatedMap:
        for distance in estimatedMap.get(angle):
            if distance > 0:
                x[angle] = - distance * math.cos(math.radians(angle))
                y[angle] = distance * math.sin(math.radians(angle))
        
    axe.clear()
    axe.scatter(x, y, c='b', s=5)
    axe.scatter(0, 0, c='r', s=5)
    axe.set_ylim(-6000, 6000)
    axe.set_xlim(-6000, 6000)
    fig.canvas.draw_idle()
    plt.savefig('1.png')


def move(distance):
    bot.drive_direct(225, 225)
    time.sleep(distance * 3)
    bot.drive_stop()


def rotate(angle):
    if angle > 0:
        bot.drive_direct(-150, 150)
    elif angle == 0:
        bot.drive_direct(0, 0)
    else:
        angle = -angle
        bot.drive_direct(150, -150)
    time.sleep(angle/72)
    bot.drive_stop()


def disconnect():
    bot.close()


connect()
print('connected')

command = ''
while 'disconnect' not in command:
    prev_com = command

    if 'scan' in command:
        scanMap()
        print('scanned')

    elif 'move' in command:
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
