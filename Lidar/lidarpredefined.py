import PyLidar3
import matplotlib.pyplot as plt
import matplotlib
import math
import statistics
import time


# Scan, process, & map lidar data
def scanMap():
    port = '/dev/ttyUSB1'
    curScan = []
    allScans = {}
    
    # Connection to lidar
    Obj = PyLidar3.YdLidarX4(port, chunk_size=6000)
    if Obj.Connect():
        gen = Obj.StartScanning()
        # Number of scans to be taken
        for i in range(10):     # rp#ScanNum
            curScan = next(gen)
            for angle in range(0,360):
                if angle not in allScans.keys():
                    allScans.update({angle: [curScan[angle]]})
                else:
                    allScans[angle].append(curScan[angle])
        
        # Disconnect from lidar
        Obj.Disconnect()
    
    # Process scan data
    meanScan = {}
    stdevScan = {}
    varScan = {}
    
    # Take mean, variance, & standard diviation of scans
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
    
    # Map lidar scan & save as image (.png)

    fig = plt.figure(1)
    
    fig.canvas.manager.set_window_title("Pi#1") # "pi#" + piNum + " | map " + mapRp#
    axe = fig.add_subplot(111)
    plt.cla()
    
    x = [0 for _ in range(360)]
    y = [0 for _ in range(360)]
    
    for angle in acceptedScan:
        for distance in acceptedScan.get(angle):
            if distance > 0:
                x[angle] = - distance * math.cos(math.radians(angle))
                y[angle] = distance * math.sin(math.radians(angle))
        
    axe.clear()
    axe.scatter(x, y, c='b', s=5)
    axe.scatter(0, 0, c='r', s=5)
    axe.set_ylim(-6000, 6000)
    axe.set_xlim(-6000, 6000)
    fig.canvas.draw_idle()
    plt.savefig('1.png') # mapRp# + '.png'

scanMap()