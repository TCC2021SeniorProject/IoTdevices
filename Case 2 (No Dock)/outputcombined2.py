import asyncio
import time
import piInterface as piI

numLoops = 0
initalize = None #Channel variable
undock = None #Channel variable
dock = None #Channel variable
scan = None #Channel variable
turn = None #Channel variable
map = None #Channel variable
finish = None #Channel variable
move = None #Channel variable
disconnect = None #Channel variable
rp0On = False
rp1On = False
rp0State = 0
rp1State = 0
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
        pass

    async def Com_disconnect(self):
        pi0, pi1 = piI.ShellBoth('disconnect')
        while 'disconnected' not in pi0:
            time.sleep(.1)
            pi0 = piI.Shell('', 0)
        while 'disconnected' not in pi1:
            time.sleep(.1)
            pi1 = piI.Shell('', 1)
        piI.Disconnect()

        pass

    async def Com_finished(self):
        global numLoops
        if numLoops < 2:
            numLoops = numLoops +1
            await asyncio.sleep(0.01)
            await asyncio.gather(Pi0.Finishing(), Pi1.Finishing(), )
            await self.Com_initialized()
        if numLoops == 2:
            await asyncio.sleep(0.01)
            await asyncio.gather(Pi0.Disconnecting(), Pi1.Disconnecting(), )
            await self.Com_disconnect()

    async def Com_turn5(self):
        global rp0Angle
        rp0Angle = -90.0
        global rp1Angle
        rp1Angle = 90.0
        await asyncio.sleep(0.01)
        await asyncio.gather(Pi0.Turning(), Pi1.Turning(), )
        await self.Com_finished()

    async def Com_scan2(self):
        global rp0ScanNum
        rp0ScanNum = 25
        global rp1ScanNum
        rp1ScanNum = 25
        global mapRp0
        mapRp0 = numLoops +2
        global mapRp1
        mapRp1 = numLoops +2
        await asyncio.sleep(0.01)
        await asyncio.gather(Pi0.Scanning(), Pi1.Scanning(), )
        await self.Com_turn5()

    async def Com_move4(self):
        global rp0Distance
        rp0Distance = 1.0
        global rp1Distance
        rp1Distance = 1.0
        await asyncio.sleep(0.01)
        await asyncio.gather(Pi0.Moving(), Pi1.Moving(), )
        await self.Com_scan2()

    async def Com_turn4(self):
        global rp0Angle
        rp0Angle = 90.0
        global rp1Angle
        rp1Angle = -90.0
        await asyncio.sleep(0.01)
        await asyncio.gather(Pi0.Turning(), Pi1.Turning(), )
        await self.Com_move4()

    async def Com_move3(self):
        global rp0Distance
        rp0Distance = 1.0
        global rp1Distance
        rp1Distance = 1.0
        await asyncio.sleep(0.01)
        await asyncio.gather(Pi0.Moving(), Pi1.Moving(), )
        await self.Com_turn4()

    async def Com_scan1(self):
        global rp0ScanNum
        rp0ScanNum = 25
        global rp1ScanNum
        rp1ScanNum = 25
        global mapRp0
        mapRp0 = numLoops +1
        global mapRp1
        mapRp1 = numLoops +1
        await asyncio.sleep(0.01)
        await asyncio.gather(Pi0.Scanning(), Pi1.Scanning(), )
        await self.Com_move3()

    async def Com_turn3(self):
        global rp0Angle
        rp0Angle = 90.0
        global rp1Angle
        rp1Angle = -90.0
        await asyncio.sleep(0.01)
        await asyncio.gather(Pi0.Turning(), Pi1.Turning(), )
        await self.Com_scan1()

    async def Com_move2(self):
        global rp0Distance
        rp0Distance = 1.0
        global rp1Distance
        rp1Distance = 1.0
        await asyncio.sleep(0.01)
        await asyncio.gather(Pi0.Moving(), Pi1.Moving(), )
        await self.Com_turn3()

    async def Com_turn2(self):
        global rp0Angle
        rp0Angle = 90.0
        global rp1Angle
        rp1Angle = -90.0
        await asyncio.sleep(0.01)
        await asyncio.gather(Pi0.Turning(), Pi1.Turning(), )
        await self.Com_move2()

    async def Com_move1(self):
        global rp0Distance
        rp0Distance = 1.0
        global rp1Distance
        rp1Distance = 1.0
        await asyncio.sleep(0.01)
        await asyncio.gather(Pi0.Moving(), Pi1.Moving(), )
        await self.Com_turn2()

    async def Com_turn1(self):
        global rp0Angle
        rp0Angle = 180.0
        global rp1Angle
        rp1Angle = -180.0
        await asyncio.sleep(0.01)
        await asyncio.gather(Pi0.Turning(), Pi1.Turning(), )
        await self.Com_move1()

    async def Com_initialized(self):
        piI.Connect()
        pi0, pi1 = piI.ShellBoth('python3 -i predefined2.py\n')
        print(str(pi0) + '\n' + str(pi1))
        while 'connected' not in pi0:
            time.sleep(.1)
            pi0 = piI.Shell('', 0)
            print(pi0)
        while 'connected' not in pi1:
            time.sleep(.1)
            pi1 = piI.Shell('', 1)
            print(pi1)

        await asyncio.sleep(0.01)
        await asyncio.gather(Pi0.Initializing(), Pi1.Initializing(), )
        await self.Com_turn1()

class RaspberryPi0:
    def __init__(self, ):
        global CC
        global Pi1
        self.piNum = 0

    async def Finished(self):
        pass

    async def Finishing(self):
        await asyncio.sleep(0.01)
        await self.Finished()

    async def Undocked(self):
        pass

    async def Undocking(self):
        await asyncio.sleep(0.01)
        await self.Undocked()

    async def Turned(self):
        pass

    async def Turning(self):
        if self.piNum == 0:
            out = piI.Shell('rotate ' + str(rp0Angle), self.piNum)
        else:
            out = piI.Shell('rotate ' + str(rp1Angle), self.piNum)
        print(out)
        await asyncio.sleep(0.01)
        while 'rotated' not in out:
            time.sleep(.1)
            out = piI.Shell('', self.piNum)
            print(out)

        await asyncio.sleep(0.01)
        await self.Turned()

    async def Moved(self):
        pass

    async def Moving(self):
        if self.piNum == 0:
            out = piI.Shell('move ' + str(rp0Distance), self.piNum)
        else:
            out = piI.Shell('move ' + str(rp1Distance), self.piNum)
        print(out)
        await asyncio.sleep(0.01)
        while 'moved' not in out:
            time.sleep(.1)
            out = piI.Shell('', self.piNum)
            print(out)

        await asyncio.sleep(0.01)
        await self.Moved()

    async def Scanned(self):
        pass

    async def Scanning(self):
        out = piI.Shell('scan\n', self.piNum)
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

    async def Disconnected(self):
        pass

    async def Disconnecting(self):
        await asyncio.sleep(0.01)
        await self.Disconnected()

    async def Docked(self):
        pass

    async def Docking(self):
        out = piI.Shell('dock', self.piNum)
        print(out)
        await asyncio.sleep(0.01)
        while 'docked' not in out:
            time.sleep(.1)
            out = piI.Shell('', self.piNum)
            print(out)

        await asyncio.sleep(0.01)
        await self.Docked()

    async def Initialized(self):
        pass

    async def Initializing(self):
        await asyncio.sleep(0.01)
        await self.Initialized()

class RaspberryPi1:
    def __init__(self, ):
        global CC
        global Pi0
        self.piNum = 1

    async def Finished(self):
        pass

    async def Finishing(self):
        await asyncio.sleep(0.01)
        await self.Finished()

    async def Undocked(self):
        pass

    async def Undocking(self):
        await asyncio.sleep(0.01)
        await self.Undocked()

    async def Turned(self):
        pass

    async def Turning(self):
        if self.piNum == 0:
            out = piI.Shell('rotate ' + str(rp0Angle), self.piNum)
        else:
            out = piI.Shell('rotate ' + str(rp1Angle), self.piNum)
        print(out)
        await asyncio.sleep(0.01)
        while 'rotated' not in out:
            time.sleep(.1)
            out = piI.Shell('', self.piNum)
            print(out)

        await asyncio.sleep(0.01)
        await self.Turned()

    async def Moved(self):
        pass

    async def Moving(self):
        if self.piNum == 0:
            out = piI.Shell('move ' + str(rp0Distance), self.piNum)
        else:
            out = piI.Shell('move ' + str(rp1Distance), self.piNum)
        print(out)
        await asyncio.sleep(0.01)
        while 'moved' not in out:
            time.sleep(.1)
            out = piI.Shell('', self.piNum)
            print(out)

        await asyncio.sleep(0.01)
        await self.Moved()

    async def Scanned(self):
        pass

    async def Scanning(self):
        out = piI.Shell('scan\n', self.piNum)
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

    async def Disconnected(self):
        pass

    async def Disconnecting(self):
        await asyncio.sleep(0.01)
        await self.Disconnected()

    async def Docked(self):
        pass

    async def Docking(self):
        out = piI.Shell('dock', self.piNum)
        print(out)
        await asyncio.sleep(0.01)
        while 'docked' not in out:
            time.sleep(.1)
            out = piI.Shell('', self.piNum)
            print(out)

        await asyncio.sleep(0.01)
        await self.Docked()

    async def Initialized(self):
        pass

    async def Initializing(self):
        await asyncio.sleep(0.01)
        await self.Initialized()

loop = asyncio.get_event_loop()
Pi0 = RaspberryPi0()
Pi1 = RaspberryPi1()
CC = CentralController()
loop.run_until_complete(CC.Com_initialized())
loop.run_until_complete(Pi0.Initializing())
loop.run_until_complete(Pi1.Initializing())