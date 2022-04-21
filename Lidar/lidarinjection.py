def Scanning():
    if self.piNum == 0:
        com = 'scan 0 ' + str(mapRp0) + '\n'
    else:
        com = 'scan 1 ' + str(mapRp1) + '\n'
    out = piI.Shell(com, self.piNum)
    print(out, end='')
    await asyncio.sleep(0.01)
    while 'scanned' not in out:
        time.sleep(.1)
        out = piI.Shell('', self.piNum)
        print(out, end='')
    file = com[5:]
    if self.piNum == 0:
        piI.Retrieve(file, 0)
    else:
        piI.Retrieve(file, 1)
    await asyncio.sleep(0.01)