import asyncio
import time
import piInterface as piI

numLoops = 0
initialized = None #Channel variable
undock = None #Channel variable
dock = None #Channel variable
finished = None #Channel variable
move = None #Channel variable
disconnect = None #Channel variable
rp0Turn = None #Channel variable
rp1Turn = None #Channel variable
rp0Angle = 0.0
rp1Angle = 0.0
rp0Distance = 0.0
rp1Distance = 0.0

class CentralController:
    def __init__(self, ):
        global Pi0
        global Pi1
        self.numTurns = 0
        self.numLoops = 0

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

        pass

    async def Com_disconnect(self):
        await asyncio.sleep(0.01)
        await asyncio.gather(Pi0.Disconnecting(), Pi1.Disconnecting(), )
        await self.Com_finished()

    async def Com_dock(self):
        if  (self.numTurns % 2 == False) and self.numTurns < 36:
            global rp0Angle
            rp0Angle = 10.0
            await asyncio.sleep(0.01)
            await asyncio.gather(Pi0.Turning(), )
            await self.Com_turn2()
        if  (self.numTurns % 2 == True) and self.numTurns < 36:
            global rp1Angle
            rp1Angle = -10.0
            await asyncio.sleep(0.01)
            await asyncio.gather(Pi1.Turning(), )
            await self.Com_turn2()
        if self.numTurns >= 36:
            self.numTurns = 0
            await asyncio.sleep(0.01)
            await asyncio.gather(Pi0.Docking(), Pi1.Docking(), )
            await self.Com_disconnect()

    async def Com_turn2(self):
        self.numTurns = self.numTurns +1
        await asyncio.sleep(0.01)
        await self.Com_dock()

    async def Com_move(self):
        if self.numTurns >= 36:
            self.numTurns = 0
            global rp0Distance
            rp0Distance = 1.0
            global rp1Distance
            rp1Distance = 1.0
            await asyncio.sleep(0.01)
            await asyncio.gather(Pi0.Moving(), Pi1.Moving(), )
            await self.Com_turn2()
        if  (self.numTurns % 2 == False) and self.numTurns < 36:
            global rp0Angle
            rp0Angle = -10.0
            await asyncio.sleep(0.01)
            await asyncio.gather(Pi0.Turning(), )
            await self.Com_turn1()
        if  (self.numTurns % 2 == True) and self.numTurns < 36:
            global rp1Angle
            rp1Angle = 10.0
            await asyncio.sleep(0.01)
            await asyncio.gather(Pi1.Turning(), )
            await self.Com_turn1()

    async def Com_turn1(self):
        self.numTurns = self.numTurns +1
        await asyncio.sleep(0.01)
        await self.Com_move()

    async def Com_undock(self):
        global rp0Distance
        rp0Distance = -0.1
        global rp1Distance
        rp1Distance = -0.1
        await asyncio.sleep(0.01)
        await asyncio.gather(Pi0.Undock(), Pi1.Undock(), )
        await self.Com_turn1()

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
        await asyncio.gather(Pi0.Initalized(), Pi1.Initalized(), )
        await self.Com_undock()

class RaspberryPi0:
    def __init__(self, ):
        global CC
        global Pi1
        self.piNum = 0

    async def Empty1(self):
        pass

    async def Finished(self):
        await asyncio.sleep(0.01)
        await self.Empty1()

    async def Empty2(self):
        pass

    async def Initalized(self):
        await asyncio.sleep(0.01)
        await self.Empty2()

    async def Empty3(self):
        pass

    async def Moving(self):
        if self.piNum == 0:
            out = piI.Shell('move ' + str(rp0Distance), self.piNum)
        else:
            out = piI.Shell('move ' + str(rp1Distance), self.piNum)
        print(out, end='')
        await asyncio.sleep(0.01)
        while 'moved' not in out:
            time.sleep(.1)
            out = piI.Shell('', self.piNum)
            print(out, end='')

        await asyncio.sleep(0.01)
        await self.Empty3()

    async def Empty4(self):
        pass

    async def Undock(self):
        out = piI.Shell('undock\n', self.piNum)
        print(out, end='')
        await asyncio.sleep(0.01)
        while 'undocked' not in out:
            time.sleep(.1)
            out = piI.Shell('', self.piNum)
            print(out, end='')

        await asyncio.sleep(0.01)
        await self.Empty4()

    async def Empty7(self):
        pass

    async def Disconnecting(self):
        await asyncio.sleep(0.01)
        await self.Empty7()

    async def Empty6(self):
        pass

    async def Docking(self):
        out = piI.Shell('dock', self.piNum)
        print(out, end='')
        await asyncio.sleep(0.01)
        while 'docked' not in out:
            time.sleep(.1)
            out = piI.Shell('', self.piNum)
            print(out, end='')

        await asyncio.sleep(0.01)
        await self.Empty6()

    async def Empty5(self):
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
        await self.Empty5()

class RaspberryPi1:
    def __init__(self, ):
        global CC
        global Pi0
        self.piNum = 1

    async def Empty1(self):
        pass

    async def Finished(self):
        await asyncio.sleep(0.01)
        await self.Empty1()

    async def Empty2(self):
        pass

    async def Initalized(self):
        await asyncio.sleep(0.01)
        await self.Empty2()

    async def Empty3(self):
        pass

    async def Moving(self):
        if self.piNum == 0:
            out = piI.Shell('move ' + str(rp0Distance), self.piNum)
        else:
            out = piI.Shell('move ' + str(rp1Distance), self.piNum)
        print(out, end='')
        await asyncio.sleep(0.01)
        while 'moved' not in out:
            time.sleep(.1)
            out = piI.Shell('', self.piNum)
            print(out, end='')

        await asyncio.sleep(0.01)
        await self.Empty3()

    async def Empty4(self):
        pass

    async def Undock(self):
        out = piI.Shell('undock\n', self.piNum)
        print(out, end='')
        await asyncio.sleep(0.01)
        while 'undocked' not in out:
            time.sleep(.1)
            out = piI.Shell('', self.piNum)
            print(out, end='')

        await asyncio.sleep(0.01)
        await self.Empty4()

    async def Empty7(self):
        pass

    async def Disconnecting(self):
        await asyncio.sleep(0.01)
        await self.Empty7()

    async def Empty6(self):
        pass

    async def Docking(self):
        out = piI.Shell('dock', self.piNum)
        print(out, end='')
        await asyncio.sleep(0.01)
        while 'docked' not in out:
            time.sleep(.1)
            out = piI.Shell('', self.piNum)
            print(out, end='')

        await asyncio.sleep(0.01)
        await self.Empty6()

    async def Empty5(self):
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
        await self.Empty5()

loop = asyncio.get_event_loop()
Pi0 = RaspberryPi0()
Pi1 = RaspberryPi1()
CC = CentralController()
loop.run_until_complete(CC.Com_initialized())
loop.run_until_complete(Pi0.Initalized())
loop.run_until_complete(Pi1.Initalized())