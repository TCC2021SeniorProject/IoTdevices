import asyncio
import time
import piInterface as piI

initalize = None #Channel variable
undock = None #Channel variable
dock = None #Channel variable
disconnect = None #Channel variable
turn1 = None #Channel variable
turn2 = None #Channel variable
turn3 = None #Channel variable
turn4 = None #Channel variable
turn5 = None #Channel variable
move1 = None #Channel variable
move2 = None #Channel variable
move3 = None #Channel variable
move4 = None #Channel variable
move5 = None #Channel variable
rp0On = False
rp1On = False
rp0State = 0
rp1State = 0
rp0Angle = 0.0
rp1Angle = 0.0
rp0Distance = 0.0
rp1Distance = 0.0
scan1 = None #Channel variable
scan2 = None #Channel variable
map1 = None #Channel variable
map2 = None #Channel variable
rp0ScanTime = 0.0
rp1ScanTime = 0.0
map1Rp0 = 0
map1Rp1 = 0
map2Rp0 = 0
map2Rp1 = 0

class CentralController:
    def __init__(self, Pi0, Pi1):
        self.Pi0 = Pi0
        self.Pi1 = Pi1
        self.numLoops = 0

    async def Com_disconnect(self):
        print('Com_disconnect()')
        await asyncio.sleep(0.01)
        pi0, pi1 = piI.ShellBoth('disconnect')
        while 'disconnected' not in pi0:
            time.sleep(.1)
            pi0 = piI.Shell('', 0)
        while 'disconnected' not in pi1:
            time.sleep(.1)
            pi1 = piI.Shell('', 1)
        piI.Disconnect()

        self.numLoops = self.numLoops +1
        
        if self.numLoops > 0:
            Disconnecting_task_0 = loop.create_task(self.Pi0.Disconnecting())
            Disconnecting_task_1 = loop.create_task(self.Pi1.Disconnecting())
            await asyncio.wait([Disconnecting_task_0, Disconnecting_task_1, ])
            exit()
        await self.Com_initialized()

    async def Com_dock(self):
        print('Com_dock()')

        await asyncio.gather(self.Pi0.Docking(), self.Pi1.Docking())
        await self.Com_disconnect()

    async def Com_turn5(self):
        print('Com_turn5()')
        global rp0Angle
        global rp1Angle
        rp0Angle = -90.0
        rp1Angle = 90.0

        await asyncio.gather(self.Pi0.Turning5(), self.Pi1.Turning5())
        await self.Com_dock()

    async def Com_map2(self):
        print('Com_map2()')
        await asyncio.sleep(0.01)
        map2Rp0 = self.numLoops +1
        map2Rp1 = self.numLoops +1
        
        Mapping2_task_0 = loop.create_task(self.Pi0.Mapping2())
        Mapping2_task_1 = loop.create_task(self.Pi1.Mapping2())
        await asyncio.wait([Mapping2_task_0, Mapping2_task_1, ])
        await self.Com_turn5()

    async def Com_scan2(self):
        print('Com_scan2()')
        await asyncio.sleep(0.01)
        rp0ScanTime = 2.0
        rp1ScanTime = 2.0
        
        Scanning2_task_0 = loop.create_task(self.Pi0.Scanning2())
        Scanning2_task_1 = loop.create_task(self.Pi1.Scanning2())
        await asyncio.wait([Scanning2_task_0, Scanning2_task_1, ])
        await self.Com_map2()

    async def Com_move4(self):
        print('Com_move4()')
        global rp0Distance
        global rp1Distance
        rp0Distance = 1.0
        rp1Distance = 1.0
        
        await asyncio.gather(self.Pi0.Moving4(), self.Pi1.Moving4())
        await self.Com_scan2()

    async def Com_turn4(self):
        print('Com_turn4()')
        global rp0Angle
        global rp1Angle
        rp0Angle = 90.0
        rp1Angle = -90.0
        
        await asyncio.gather(self.Pi0.Turning4(), self.Pi1.Turning4())
        await self.Com_move4()

    async def Com_move3(self):
        print('Com_move3()')
        global rp0Distance
        global rp1Distance
        rp0Distance = 1.0
        rp1Distance = 1.0
        
        await asyncio.gather(self.Pi0.Moving3(), self.Pi1.Moving3())
        await self.Com_turn4()

    async def Com_map1(self):
        print('Com_map1()')
        await asyncio.sleep(0.01)
        map1Rp0 = self.numLoops +1
        map1Rp1 = self.numLoops +1
        
        Mapping1_task_0 = loop.create_task(self.Pi0.Mapping1())
        Mapping1_task_1 = loop.create_task(self.Pi1.Mapping1())
        await asyncio.wait([Mapping1_task_0, Mapping1_task_1, ])
        await self.Com_move3()

    async def Com_scan1(self):
        print('Com_scan1()')
        await asyncio.sleep(0.01)
        rp0ScanTime = 1.0
        rp1ScanTime = 1.0
        
        await self.Com_map1()

    async def Com_turn3(self):
        print('Com_turn3()')
        global rp0Angle
        global rp1Angle
        rp0Angle = 90.0
        rp1Angle = -90.0
        
        await asyncio.gather(self.Pi0.Turning3(), self.Pi1.Turning3())
        await self.Com_scan1()

    async def Com_move2(self):
        print('Com_move2()')
        global rp0Distance
        global rp1Distance
        rp0Distance = 1.0
        rp1Distance = 1.0
        
        await asyncio.gather(self.Pi0.Moving2(), self.Pi1.Moving2())
        await self.Com_turn3()

    async def Com_turn2(self):
        print('Com_turn2()')
        global rp0Angle
        global rp1Angle
        rp0Angle = 90.0
        rp1Angle = -90.0
        
        await asyncio.gather(self.Pi0.Turning2(), self.Pi1.Turning2())
        await self.Com_move2()

    async def Com_move1(self):
        print('Com_move1()')
        global rp0Distance
        global rp1Distance
        rp0Distance = 1.0
        rp1Distance = 1.0
        
        await asyncio.gather(self.Pi0.Moving1(), self.Pi1.Moving1())
        await self.Com_turn2()

    async def Com_turn1(self):
        print('Com_turn1()')
        global rp0Angle
        global rp1Angle
        rp0Angle = 180.0
        rp1Angle = -180.0
        
        await asyncio.gather(self.Pi0.Turning1(), self.Pi1.Turning1())
        await self.Com_move1()

    async def Com_undock(self):
        print('Com_undock()')
        rp0Distance = -0.1
        rp1Distance = -0.1

        await asyncio.gather(self.Pi0.Undock(), self.Pi1.Undock())
        await self.Com_turn1()

    async def Com_initialized(self):
        print('Com_initialized()')
        await asyncio.sleep(0.01)
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

        Initalized_task_0 = loop.create_task(self.Pi0.Initalized())
        Initalized_task_1 = loop.create_task(self.Pi1.Initalized())
        await asyncio.wait([Initalized_task_0, Initalized_task_1, ])
        await self.Com_undock()

class RaspberryPi0:
    def __init__(self, ):
        self.piNum = 0

    async def Disconnecting(self):
        print('Pi0 Disconnecting()')
        await asyncio.sleep(0.01)
        #await self.Undock()

    async def Docking(self):
        print('Pi0 Docking()')
        out = piI.Shell('dock', self.piNum)
        print(out)
        await asyncio.sleep(0.01)
        while 'docked' not in out:
            time.sleep(.1)
            out = piI.Shell('', self.piNum)
            print(out)

    async def Turning5(self):
        print('Pi0 Turning5()')
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

    async def Mapping2(self):
        print('Pi0 Mapping2()')
        await asyncio.sleep(0.01)
        #Com_map2_task_0 = loop.create_task(CentralController().Com_map2())
        #await asyncio.wait([Com_map2_task_0, ])
        #await self.Turning5()

    async def Scanning2(self):
        print('Pi0 Scanning2()')
        await asyncio.sleep(0.01)
        #await self.Mapping2()

    async def Moving4(self):
        print('Pi0 Moving4()')
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

    async def Turning4(self):
        print('Pi0 Turning4()')
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

    async def Moving3(self):
        print('Pi0 Moving3()')
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

    async def Mapping1(self):
        print('Pi0 Mapping1()')
        await asyncio.sleep(0.01)
        #await self.Moving3()

    async def Scanning1(self):
        print('Pi0 Scanning1()')
        await asyncio.sleep(0.01)
        #Com_scan1_task_0 = loop.create_task(CentralController().Com_scan1())
        #await asyncio.wait([Com_scan1_task_0, ])
        #await self.Mapping1()

    async def Turning3(self):
        print('Pi0 Turning3()')
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

    async def Moving2(self):
        print('Pi0 Moving2()')
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

    async def Turning2(self):
        print('Pi0 Turning2()')
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

    async def Moving1(self):
        print('Pi0 Moving1()')
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

    async def Turning1(self):
        print('Pi0 Turning1()')
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

    async def Undock(self):
        print('Pi0 Undock()')
        out = piI.Shell('undock\n', self.piNum)
        print(out)
        await asyncio.sleep(0.01)
        while 'undocked' not in out:
            time.sleep(.1)
            out = piI.Shell('', self.piNum)
            print(out)

    async def Initalized(self):
        print('Pi0 Initialized()')
        await asyncio.sleep(0.01)
        rp0On = True
        
        #await self.Undock()

class RaspberryPi1:
    def __init__(self, ):
        self.piNum = 1

    async def Disconnecting(self):
        print('Pi1 Disconnecting()')
        await asyncio.sleep(0.01)
        #await self.Undock()

    async def Docking(self):
        print('Pi1 Docking()')
        out = piI.Shell('dock', self.piNum)
        print(out)
        await asyncio.sleep(0.01)
        while 'docked' not in out:
            time.sleep(.1)
            out = piI.Shell('', self.piNum)
            print(out)

    async def Turning5(self):
        print('Pi1 Turning5()')
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

    async def Mapping2(self):
        print('Pi1 Mapping2()')
        await asyncio.sleep(0.01)
        #Com_map2_task_0 = loop.create_task(CentralController().Com_map2())
        #await asyncio.wait([Com_map2_task_0, ])
        #await self.Turning5()

    async def Scanning2(self):
        print('Pi1 Scanning2()')
        await asyncio.sleep(0.01)
        #await self.Mapping2()

    async def Moving4(self):
        print('Pi1 Moving4()')
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

    async def Turning4(self):
        print('Pi1 Turning4()')
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

    async def Moving3(self):
        print('Pi1 Moving3()')
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

    async def Mapping1(self):
        print('Pi1 Mapping1()')
        await asyncio.sleep(0.01)
        #await self.Moving3()

    async def Scanning1(self):
        print('Pi1 Scanning1()')
        await asyncio.sleep(0.01)
        #Com_scan1_task_0 = loop.create_task(CentralController().Com_scan1())
        #await asyncio.wait([Com_scan1_task_0, ])
        #await self.Mapping1()

    async def Turning3(self):
        print('Pi1 Turning3()')
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

    async def Moving2(self):
        print('Pi1 Moving2()')
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

    async def Turning2(self):
        print('Pi1 Turning2()')
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

    async def Moving1(self):
        print('Pi1 Moving1()')
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

    async def Turning1(self):
        print('Pi1 Turning1()')
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

    async def Undock(self):
        print('Pi1 Undock()')
        out = piI.Shell('undock\n', self.piNum)
        print(out)
        await asyncio.sleep(0.01)
        while 'undocked' not in out:
            time.sleep(.1)
            out = piI.Shell('', self.piNum)
            print(out)

    async def Initalized(self):
        print('Pi1 Initialized()')
        await asyncio.sleep(0.01)
        rp1On = True
        
        #await self.Undock()

loop = asyncio.get_event_loop()
Pi0 = RaspberryPi0()
Pi1 = RaspberryPi1()
CC = CentralController(Pi0, Pi1)
try:
    loop.run_until_complete(CC.Com_initialized())
    loop.run_until_complete(loop.shutdown_asyncgens())
finally:
    loop.close()