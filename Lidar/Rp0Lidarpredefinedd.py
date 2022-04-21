import PyLidar3
import matplotlib.pyplot as plt
import math
import statistics
import time


# Scan, process, map, and save lidar scans as local image
def scanMap(mapRP0, rp0ScanNum):
    
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
        # Loop for rp0ScanNum seconds while scanning
        while(time.time() - startTime) < rp0ScanNum:     # rp#ScanNum
            
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
    
    fig.canvas.manager.set_window_title("Lidar Map | pi0 - " + mapRp0)
    
    x = [0 for _ in range(360)]
    y = [0 for _ in range(360)]
    
    for angle in acceptedScan:
        for distance in acceptedScan.get(angle):
            x[angle] = - distance * math.cos(math.radians(angle))
            y[angle] = distance * math.sin(math.radians(angle))
    
    plt.scatter(x, y, marker='s', c='blue', alpha=0.7, s=10)
    plt.plot(0,0, marker='o', markersize=7, markerfacecolor='grey', mew=1.0, markeredgecolor='black')
    fig.canvas.draw()

    plt.savefig('pi0' + '_' + mapRp0 + '.png')
