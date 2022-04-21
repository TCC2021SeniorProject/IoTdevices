import asyncio
import time
import piInterface as piI

numLoops = 0
initalize = None #Channel variable
turn = None #Channel variable
move = None #Channel variable
scan = None #Channel variable
finish = None #Channel variable
disconnect = None #Channel variable
rp0Angle = 0.0
rp1Angle = 0.0
rp0Distance = 0.0
rp1Distance = 0.0
rp0ScanNum = 0
rp1ScanNum = 0
mapRp0 = 0
mapRp1 = 0

class CentralController:
    def __init__(self, ):
        global Pi0
        global Pi1
        self.numTurns = 0
        self.numLoops = 0

    async def Com_disconnect(self):
        pass

    async def Com_finished(self):
        pi0, pi1 = piI.ShellBoth('disconnect')
        while 'disconnected' not in pi0:
            time.sleep(.1)
            pi0 = piI.Shell('', 0)
        while 'disconnected' not in pi1:
            time.sleep(.1)
            pi1 = piI.Shell('', 1)
        piI.Disconnect()
        time.sleep(3)

        if self.numLoops == 4:
            await asyncio.sleep(0.01)
            await asyncio.gather(Pi0.Disconnecting(), Pi1.Disconnecting(), )
            await self.Com_disconnect()
        if self.numLoops < 4:
            self.numLoops = numLoops +1
            await asyncio.sleep(0.01)
            await asyncio.gather()
            await self.Com_initialized()

    async def Com_scan1(self):
        global rp0ScanNum
        rp0ScanNum = 5
        global rp1ScanNum
        rp1ScanNum = 5
        global mapRp0
        mapRp0 = numLoops +1
        global mapRp1
        mapRp1 = numLoops +1
        await asyncio.sleep(0.01)
        await asyncio.gather(Pi0.Scanning(), Pi1.Scanning(), )
        await self.Com_finished()

    async def Com_turn1(self):
        global rp0Angle
        rp0Angle = 90.0
        global rp1Angle
        rp1Angle = 90.0
        await asyncio.sleep(0.01)
        await asyncio.gather(Pi0.Turning(), Pi1.Turning(), )
        await self.Com_scan1()

    async def Com_initialized(self):
        piI.Connect()
        pi0, pi1 = piI.ShellBoth('python3 -i predefined2.py\n')
        print(str(pi0) + str(pi1), end='')
        while 'connected' not in pi0:
            time.sleep(.1)
            pi0 = piI.Shell('', 0)
            print(pi0, end='')
        while 'connected' not in pi1:
            time.sleep(.1)
            pi1 = piI.Shell('', 1)

        await asyncio.sleep(0.01)
        await asyncio.gather(Pi0.Initializing(), Pi1.Initializing(), )
        await self.Com_turn1()

class RaspberryPi0:
    def __init__(self, ):
        global CC
        global Pi1
        self.piNum = 0

    async def Initialized(self):
        pass

    async def Initializing(self):
        await asyncio.sleep(0.01)
        await self.Initialized()

    async def Disconnected(self):
        pass

    async def Disconnecting(self):
        await asyncio.sleep(0.01)
        await self.Disconnected()

    async def Scanned(self):
        pass

    async def Scanning(self):
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
        await self.Scanned()

    async def Turned(self):
        pass

    async def Turning(self):
        if self.piNum == 0:
            out = piI.Shell('rotate ' + str(rp0Angle), self.piNum)
        else:
            out = piI.Shell('rotate ' + str(rp1Angle), self.piNum)
        print(out, end='')
        await asyncio.sleep(0.01)
        while 'rotated' not in out:
            time.sleep(.1)
            out = piI.Shell('', self.piNum)
            print(out, end='')

        await asyncio.sleep(0.01)
        await self.Turned()

class RaspberryPi1:
    def __init__(self, ):
        global CC
        global Pi0
        self.piNum = 1

    async def Initialized(self):
        pass

    async def Initializing(self):
        await asyncio.sleep(0.01)
        await self.Initialized()

    async def Disconnected(self):
        pass

    async def Disconnecting(self):
        await asyncio.sleep(0.01)
        await self.Disconnected()

    async def Scanned(self):
        pass

    async def Scanning(self):
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
        await self.Scanned()

    async def Turned(self):
        pass

    async def Turning(self):
        if self.piNum == 0:
            out = piI.Shell('rotate ' + str(rp0Angle), self.piNum)
        else:
            out = piI.Shell('rotate ' + str(rp1Angle), self.piNum)
        print(out, end='')
        await asyncio.sleep(0.01)
        while 'rotated' not in out:
            time.sleep(.1)
            out = piI.Shell('', self.piNum)
            print(out, end='')

        await asyncio.sleep(0.01)
        await self.Turned()

loop = asyncio.get_event_loop()
Pi0 = RaspberryPi0()
Pi1 = RaspberryPi1()
CC = CentralController()
loop.run_until_complete(CC.Com_initialized())
loop.run_until_complete(Pi0.Initializing())
loop.run_until_complete(Pi1.Initializing())