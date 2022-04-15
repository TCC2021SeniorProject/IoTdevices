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
        
        Disconnecting_task_0 = loop.create_task(self.Pi0.Disconnecting())
        Disconnecting_task_1 = loop.create_task(self.Pi1.Disconnecting())
        await asyncio.wait([Disconnecting_task_0, Disconnecting_task_1, ])
        await self.Com_undock()

    async def Com_dock(self):
        await asyncio.sleep(0.01)
        await self.Com_disconnect()

    async def Com_turn5(self):
        await asyncio.sleep(0.01)
        rp0Angle = -90.0
        rp1Angle = 90.0
        
        Turning5_task_0 = loop.create_task(self.Pi0.Turning5())
        Turning5_task_1 = loop.create_task(self.Pi1.Turning5())
        await asyncio.wait([Turning5_task_0, Turning5_task_1, ])
        await self.Com_dock()

    async def Com_map2(self):
        await asyncio.sleep(0.01)
        map2Rp0 = self.numLoops +1
        map2Rp1 = self.numLoops +1
        
        await self.Com_turn5()

    async def Com_scan2(self):
        await asyncio.sleep(0.01)
        rp0ScanTime = 2.0
        rp1ScanTime = 2.0
        
        Scanning2_task_0 = loop.create_task(self.Pi0.Scanning2())
        Scanning2_task_1 = loop.create_task(self.Pi1.Scanning2())
        await asyncio.wait([Scanning2_task_0, Scanning2_task_1, ])
        await self.Com_map2()

    async def Com_move4(self):
        await asyncio.sleep(0.01)
        rp0Distance = 1.0
        rp1Distance = 1.0
        
        await self.Com_scan2()

    async def Com_turn4(self):
        await asyncio.sleep(0.01)
        rp0Angle = 90.0
        rp1Angle = -90.0
        
        Turning4_task_0 = loop.create_task(self.Pi0.Turning4())
        Turning4_task_1 = loop.create_task(self.Pi1.Turning4())
        await asyncio.wait([Turning4_task_0, Turning4_task_1, ])
        await self.Com_move4()

    async def Com_move3(self):
        await asyncio.sleep(0.01)
        rp0Distance = 1.0
        rp1Distance = 1.0
        
        await self.Com_turn4()

    async def Com_map1(self):
        await asyncio.sleep(0.01)
        map1Rp0 = self.numLoops +1
        map1Rp1 = self.numLoops +1
        
        Mapping1_task_0 = loop.create_task(self.Pi0.Mapping1())
        Mapping1_task_1 = loop.create_task(self.Pi1.Mapping1())
        await asyncio.wait([Mapping1_task_0, Mapping1_task_1, ])
        await self.Com_move3()

    async def Com_scan1(self):
        await asyncio.sleep(0.01)
        rp0ScanTime = 1.0
        rp1ScanTime = 1.0
        
        await self.Com_map1()

    async def Com_turn3(self):
        await asyncio.sleep(0.01)
        rp0Angle = 90.0
        rp1Angle = -90.0
        
        Turning3_task_0 = loop.create_task(self.Pi0.Turning3())
        Turning3_task_1 = loop.create_task(self.Pi1.Turning3())
        await asyncio.wait([Turning3_task_0, Turning3_task_1, ])
        await self.Com_scan1()

    async def Com_move2(self):
        await asyncio.sleep(0.01)
        rp0Distance = 1.0
        rp1Distance = 1.0
        
        await self.Com_turn3()

    async def Com_turn2(self):
        await asyncio.sleep(0.01)
        rp0Angle = 90.0
        rp1Angle = -90.0
        
        Turning2_task_0 = loop.create_task(self.Pi0.Turning2())
        Turning2_task_1 = loop.create_task(self.Pi1.Turning2())
        await asyncio.wait([Turning2_task_0, Turning2_task_1, ])
        await self.Com_move2()

    async def Com_move1(self):
        await asyncio.sleep(0.01)
        rp0Distance = 1.0
        rp1Distance = 1.0
        
        await self.Com_turn2()

    async def Com_turn1(self):
        await asyncio.sleep(0.01)
        rp0Angle = 180.0
        rp1Angle = -180.0
        
        Turning1_task_0 = loop.create_task(self.Pi0.Turning1())
        Turning1_task_1 = loop.create_task(self.Pi1.Turning1())
        await asyncio.wait([Turning1_task_0, Turning1_task_1, ])
        await self.Com_move1()

    async def Com_undock(self):
        await asyncio.sleep(0.01)
        rp0Distance = -0.1
        rp1Distance = -0.1
        
        await self.Com_turn1()

    async def Com_initialized(self):
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
        await asyncio.sleep(0.01)
        await self.Undock()

    async def Docking(self):
        await asyncio.sleep(0.01)
        out = piI.Shell('dock', self.piNum)
        print(out)
        while 'docked' not in out:
            time.sleep(.1)
            out = piI.Shell('', self.piNum)
            print(out)

        Com_dock_task_0 = loop.create_task(CentralController().Com_dock())
        await asyncio.wait([Com_dock_task_0, ])
        await self.Disconnecting()

    async def Turning5(self):
        await asyncio.sleep(0.01)
        if self.piNum == 0:
            out = piI.Shell('rotate ' + str(rp0Angle), self.piNum)
        else:
            out = piI.Shell('rotate ' + str(rp1Angle), self.piNum)
        print(out)
        while 'rotated' not in out:
            time.sleep(.1)
            out = piI.Shell('', self.piNum)
            print(out)

        await self.Docking()

    async def Mapping2(self):
        await asyncio.sleep(0.01)
        Com_map2_task_0 = loop.create_task(CentralController().Com_map2())
        await asyncio.wait([Com_map2_task_0, ])
        await self.Turning5()

    async def Scanning2(self):
        await asyncio.sleep(0.01)
        await self.Mapping2()

    async def Moving4(self):
        await asyncio.sleep(0.01)
        if self.piNum == 0:
            out = piI.Shell('move ' + str(rp0Distance), self.piNum)
        else:
            out = piI.Shell('move ' + str(rp1Distance), self.piNum)
        print(out)
        while 'moved' not in out:
            time.sleep(.1)
            out = piI.Shell('', self.piNum)
            print(out)

        Com_move4_task_0 = loop.create_task(CentralController().Com_move4())
        await asyncio.wait([Com_move4_task_0, ])
        await self.Scanning2()

    async def Turning4(self):
        await asyncio.sleep(0.01)
        if self.piNum == 0:
            out = piI.Shell('rotate ' + str(rp0Angle), self.piNum)
        else:
            out = piI.Shell('rotate ' + str(rp1Angle), self.piNum)
        print(out)
        while 'rotated' not in out:
            time.sleep(.1)
            out = piI.Shell('', self.piNum)
            print(out)

        await self.Moving4()

    async def Moving3(self):
        await asyncio.sleep(0.01)
        if self.piNum == 0:
            out = piI.Shell('move ' + str(rp0Distance), self.piNum)
        else:
            out = piI.Shell('move ' + str(rp1Distance), self.piNum)
        print(out)
        while 'moved' not in out:
            time.sleep(.1)
            out = piI.Shell('', self.piNum)
            print(out)

        Com_move3_task_0 = loop.create_task(CentralController().Com_move3())
        await asyncio.wait([Com_move3_task_0, ])
        await self.Turning4()

    async def Mapping1(self):
        await asyncio.sleep(0.01)
        await self.Moving3()

    async def Scanning1(self):
        await asyncio.sleep(0.01)
        Com_scan1_task_0 = loop.create_task(CentralController().Com_scan1())
        await asyncio.wait([Com_scan1_task_0, ])
        await self.Mapping1()

    async def Turning3(self):
        await asyncio.sleep(0.01)
        if self.piNum == 0:
            out = piI.Shell('rotate ' + str(rp0Angle), self.piNum)
        else:
            out = piI.Shell('rotate ' + str(rp1Angle), self.piNum)
        print(out)
        while 'rotated' not in out:
            time.sleep(.1)
            out = piI.Shell('', self.piNum)
            print(out)

        await self.Scanning1()

    async def Moving2(self):
        await asyncio.sleep(0.01)
        if self.piNum == 0:
            out = piI.Shell('move ' + str(rp0Distance), self.piNum)
        else:
            out = piI.Shell('move ' + str(rp1Distance), self.piNum)
        print(out)
        while 'moved' not in out:
            time.sleep(.1)
            out = piI.Shell('', self.piNum)
            print(out)

        Com_move2_task_0 = loop.create_task(CentralController().Com_move2())
        await asyncio.wait([Com_move2_task_0, ])
        await self.Turning3()

    async def Turning2(self):
        await asyncio.sleep(0.01)
        if self.piNum == 0:
            out = piI.Shell('rotate ' + str(rp0Angle), self.piNum)
        else:
            out = piI.Shell('rotate ' + str(rp1Angle), self.piNum)
        print(out)
        while 'rotated' not in out:
            time.sleep(.1)
            out = piI.Shell('', self.piNum)
            print(out)

        await self.Moving2()

    async def Moving1(self):
        await asyncio.sleep(0.01)
        if self.piNum == 0:
            out = piI.Shell('move ' + str(rp0Distance), self.piNum)
        else:
            out = piI.Shell('move ' + str(rp1Distance), self.piNum)
        print(out)
        while 'moved' not in out:
            time.sleep(.1)
            out = piI.Shell('', self.piNum)
            print(out)

        Com_move1_task_0 = loop.create_task(CentralController().Com_move1())
        await asyncio.wait([Com_move1_task_0, ])
        await self.Turning2()

    async def Turning1(self):
        await asyncio.sleep(0.01)
        if self.piNum == 0:
            out = piI.Shell('rotate ' + str(rp0Angle), self.piNum)
        else:
            out = piI.Shell('rotate ' + str(rp1Angle), self.piNum)
        print(out)
        while 'rotated' not in out:
            time.sleep(.1)
            out = piI.Shell('', self.piNum)
            print(out)

        await self.Moving1()

    async def Undock(self):
        await asyncio.sleep(0.01)
        out = piI.Shell('undock\n', self.piNum)
        print(out)
        while 'undocked' not in out:
            time.sleep(.1)
            out = piI.Shell('', self.piNum)
            print(out)

        if rp0On == True:
            Com_undock_task_0 = loop.create_task(CentralController().Com_undock())
            await asyncio.wait([Com_undock_task_0, ])
            await self.Turning1()

    async def Initalized(self):
        await asyncio.sleep(0.01)
        rp0On = True
        
        await self.Undock()

class RaspberryPi1:
    def __init__(self, ):
        self.piNum = 1

    async def Disconnecting(self):
        await asyncio.sleep(0.01)
        await self.Undock()

    async def Docking(self):
        await asyncio.sleep(0.01)
        out = piI.Shell('dock', self.piNum)
        print(out)
        while 'docked' not in out:
            time.sleep(.1)
            out = piI.Shell('', self.piNum)
            print(out)

        Com_dock_task_0 = loop.create_task(CentralController().Com_dock())
        await asyncio.wait([Com_dock_task_0, ])
        await self.Disconnecting()

    async def Turning5(self):
        await asyncio.sleep(0.01)
        if self.piNum == 0:
            out = piI.Shell('rotate ' + str(rp0Angle), self.piNum)
        else:
            out = piI.Shell('rotate ' + str(rp1Angle), self.piNum)
        print(out)
        while 'rotated' not in out:
            time.sleep(.1)
            out = piI.Shell('', self.piNum)
            print(out)

        await self.Docking()

    async def Mapping2(self):
        await asyncio.sleep(0.01)
        Com_map2_task_0 = loop.create_task(CentralController().Com_map2())
        await asyncio.wait([Com_map2_task_0, ])
        await self.Turning5()

    async def Scanning2(self):
        await asyncio.sleep(0.01)
        await self.Mapping2()

    async def Moving4(self):
        await asyncio.sleep(0.01)
        if self.piNum == 0:
            out = piI.Shell('move ' + str(rp0Distance), self.piNum)
        else:
            out = piI.Shell('move ' + str(rp1Distance), self.piNum)
        print(out)
        while 'moved' not in out:
            time.sleep(.1)
            out = piI.Shell('', self.piNum)
            print(out)

        Com_move4_task_0 = loop.create_task(CentralController().Com_move4())
        await asyncio.wait([Com_move4_task_0, ])
        await self.Scanning2()

    async def Turning4(self):
        await asyncio.sleep(0.01)
        if self.piNum == 0:
            out = piI.Shell('rotate ' + str(rp0Angle), self.piNum)
        else:
            out = piI.Shell('rotate ' + str(rp1Angle), self.piNum)
        print(out)
        while 'rotated' not in out:
            time.sleep(.1)
            out = piI.Shell('', self.piNum)
            print(out)

        await self.Moving4()

    async def Moving3(self):
        await asyncio.sleep(0.01)
        if self.piNum == 0:
            out = piI.Shell('move ' + str(rp0Distance), self.piNum)
        else:
            out = piI.Shell('move ' + str(rp1Distance), self.piNum)
        print(out)
        while 'moved' not in out:
            time.sleep(.1)
            out = piI.Shell('', self.piNum)
            print(out)

        Com_move3_task_0 = loop.create_task(CentralController().Com_move3())
        await asyncio.wait([Com_move3_task_0, ])
        await self.Turning4()

    async def Mapping1(self):
        await asyncio.sleep(0.01)
        await self.Moving3()

    async def Scanning1(self):
        await asyncio.sleep(0.01)
        Com_scan1_task_0 = loop.create_task(CentralController().Com_scan1())
        await asyncio.wait([Com_scan1_task_0, ])
        await self.Mapping1()

    async def Turning3(self):
        await asyncio.sleep(0.01)
        if self.piNum == 0:
            out = piI.Shell('rotate ' + str(rp0Angle), self.piNum)
        else:
            out = piI.Shell('rotate ' + str(rp1Angle), self.piNum)
        print(out)
        while 'rotated' not in out:
            time.sleep(.1)
            out = piI.Shell('', self.piNum)
            print(out)

        await self.Scanning1()

    async def Moving2(self):
        await asyncio.sleep(0.01)
        if self.piNum == 0:
            out = piI.Shell('move ' + str(rp0Distance), self.piNum)
        else:
            out = piI.Shell('move ' + str(rp1Distance), self.piNum)
        print(out)
        while 'moved' not in out:
            time.sleep(.1)
            out = piI.Shell('', self.piNum)
            print(out)

        Com_move2_task_0 = loop.create_task(CentralController().Com_move2())
        await asyncio.wait([Com_move2_task_0, ])
        await self.Turning3()

    async def Turning2(self):
        await asyncio.sleep(0.01)
        if self.piNum == 0:
            out = piI.Shell('rotate ' + str(rp0Angle), self.piNum)
        else:
            out = piI.Shell('rotate ' + str(rp1Angle), self.piNum)
        print(out)
        while 'rotated' not in out:
            time.sleep(.1)
            out = piI.Shell('', self.piNum)
            print(out)

        await self.Moving2()

    async def Moving1(self):
        await asyncio.sleep(0.01)
        if self.piNum == 0:
            out = piI.Shell('move ' + str(rp0Distance), self.piNum)
        else:
            out = piI.Shell('move ' + str(rp1Distance), self.piNum)
        print(out)
        while 'moved' not in out:
            time.sleep(.1)
            out = piI.Shell('', self.piNum)
            print(out)

        Com_move1_task_0 = loop.create_task(CentralController().Com_move1())
        await asyncio.wait([Com_move1_task_0, ])
        await self.Turning2()

    async def Turning1(self):
        await asyncio.sleep(0.01)
        if self.piNum == 0:
            out = piI.Shell('rotate ' + str(rp0Angle), self.piNum)
        else:
            out = piI.Shell('rotate ' + str(rp1Angle), self.piNum)
        print(out)
        while 'rotated' not in out:
            time.sleep(.1)
            out = piI.Shell('', self.piNum)
            print(out)

        await self.Moving1()

    async def Undock(self):
        await asyncio.sleep(0.01)
        out = piI.Shell('undock\n', self.piNum)
        print(out)
        while 'undocked' not in out:
            time.sleep(.1)
            out = piI.Shell('', self.piNum)
            print(out)

        if rp1On == True:
            Com_undock_task_0 = loop.create_task(CentralController().Com_undock())
            await asyncio.wait([Com_undock_task_0, ])
            await self.Turning1()

    async def Initalized(self):
        await asyncio.sleep(0.01)
        rp1On = True
        
        await self.Undock()

loop = asyncio.get_event_loop()
Pi0 = RaspberryPi0()
Pi1 = RaspberryPi1()
CC = CentralController()
loop.run_until_complete(CC.Com_initialized(Pi0, Pi1))
