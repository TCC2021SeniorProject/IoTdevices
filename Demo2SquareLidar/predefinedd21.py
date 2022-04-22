import time
from pycreate2 import Create2
import PyLidar3
import matplotlib.pyplot as plt
import math
import statistics
import time


def connect():
    global bot
    try:
        bot = Create2('/dev/ttyUSB0')
    except:
        bot = Create2('/dev/ttyUSB1')
    bot.start()
    bot.safe()


def move(distance):
    bot.drive_direct(225, 225)
    time.sleep(distance * 3)
    bot.drive_stop()


def scanMap(mapRp1, rp1ScanNum):
    
    # Attempt to connect to lidar on all ports (Linux)
    try:
        lidarConnection = PyLidar3.YdLidarX4('/dev/ttyUSB1', chunk_size=36000)
    except:
        lidarConnection = PyLidar3.YdLidarX4('/dev/ttyUSB0', chunk_size=36000)

    # Connection to lidar established
    if lidarConnection.Connect():
        # Current scan data
        curScan = []
        # All scan data
        allScans = {}
        
        # Begin scan
        gen = lidarConnection.StartScanning()
        
        # Get current time
        startTime = time.time()
        # Loop for rp1ScanNum seconds while scanning
        while(time.time() - startTime) < rp1ScanNum:     # rp#ScanNum
            
            # Get data form current scan
            curScan = next(gen)
            
            # Store current scan data with all scans as dict {<angle>: <distance>}
            for angle in range(0,360):
                if angle not in allScans.keys():
                    allScans.update({angle: [curScan[angle]]})
                else:
                    allScans[angle].append(curScan[angle])
        
        # Disconnect from lidar
        lidarConnection.StopScanning()
        lidarConnection.Reset()
        lidarConnection.Disconnect()
            
    
    # Connection to lidar was unable to be established
    else:
        print("Unable to connect to lidar...")
        exit(-1)
    
    # For processing data for all angles
    #  Mean 
    meanScan = {}
    # Variance 
    varScan = {}
    # Standard deviation 
    stdevScan = {}
    
    # Store mean, variance, & standard diviation
    for angle in allScans:
        meanScan.update({angle: statistics.mean(allScans.get(angle))})
        varScan.update({angle: statistics.variance(allScans.get(angle))})
        stdevScan.update({angle: statistics.stdev(allScans.get(angle))})
    
    
    # Only store distance values within standard diviation & set variance
    acceptedScan = {}
    for angle in allScans:
        for dist in allScans.get(angle):
            if (meanScan.get(angle) - stdevScan.get(angle) > dist < meanScan.get(angle) + stdevScan.get(angle)) and varScan.get(angle) < 1000:
                if angle not in acceptedScan.keys():
                    acceptedScan.update({angle: [dist]})
                else:
                    acceptedScan[angle].append(dist)
    


    # Map lidar scan & save as image (.png)
    plt.style.use('seaborn-darkgrid')
    fig = plt.figure()
    
    fig.canvas.manager.set_window_title("Lidar Map | pi1 - " + str(mapRp1))
    
    x = [0 for _ in range(360)]
    y = [0 for _ in range(360)]
    
    for angle in acceptedScan:
        for distance in acceptedScan.get(angle):
            x[angle] = - distance * math.cos(math.radians(angle))
            y[angle] = distance * math.sin(math.radians(angle))
    
    plt.scatter(x, y, marker='s', c='blue', alpha=0.7, s=10)
    plt.plot(0,0, marker='o', markersize=7, markerfacecolor='grey', mew=1.0, markeredgecolor='black')
    fig.canvas.draw()

    plt.savefig('pi1' + '_' + str(mapRp1) + '.png')


def rotate(angle):
    if angle > 0:
        bot.drive_direct(-150, 150)
    elif angle == 0:
        bot.drive_direct(0, 0)
    else:
        angle = -angle
        bot.drive_direct(150, -150)
    time.sleep(angle/67)
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

    elif 'scan' in command:
        mapRp1, rp1ScanNum = command[5:].split(' ')
        mapRp1 = int(mapRp1)
        rp1ScanNum = int(rp1ScanNum)
        scanMap(mapRp1, rp1ScanNum)
        print('scanned ' + command[5:])

    command = str(input())

disconnect()
print('disconnected')
