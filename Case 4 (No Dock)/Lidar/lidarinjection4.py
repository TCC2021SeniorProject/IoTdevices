def Scanning():
    out = piI.Shell('scanMap\n', self.piNum)
    print(out, end='')
    await asyncio.sleep(0.01)
    while 'scanned' not in out:
        time.sleep(.1)
        out = piI.Shell('', self.piNum)
        print(out, end='')
    if self.piNum == 0:
        piI.Retrieve('1.png', 0)
    else:
        piI.Retrieve('1.png', 1)
    await asyncio.sleep(0.01)
