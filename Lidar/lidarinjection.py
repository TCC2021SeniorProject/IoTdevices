def Scanning():
    if self.piNum == 0:
        com = 'scan ' + str(mapRp0) + ' ' + str(rp0ScanNum) + '\n'
    else:
        com = 'scan ' + str(mapRp1) + ' ' + str(rp1ScanNum) + '\n'
    out = piI.Shell(com, self.piNum)
    print(out, end='')
    await asyncio.sleep(0.01)
    while 'scanned' not in out:
        time.sleep(.1)
        out = piI.Shell('', self.piNum)
        print(out, end='')
    time.sleep(1)
    if self.piNum == 0:
        file0 = 'pi0_' + str(mapRp0) + '.png'
        piI.Retrieve(file0, 0)
    else:
        file1 = 'pi1_' + str(mapRp1) + '.png'
        piI.Retrieve(file1, 1)
    await asyncio.sleep(0.01)