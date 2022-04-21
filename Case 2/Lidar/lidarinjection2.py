def Scanning():
    out = piI.Shell('scanMap\n', self.piNum)
    print(out, end='')
    await asyncio.sleep(0.01)
    while 'scanned' not in out:
        time.sleep(.1)
        out = piI.Shell('', self.piNum)
        print(out, end='')
    if self.piNum == 0:
        out = piI.Retrieve(mapRp0, 0)
    else:
        out = piI.Retrieve(mapRp1, 1)
    print(out, end='')
    await asyncio.sleep(0.01)