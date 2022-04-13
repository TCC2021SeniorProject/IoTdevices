import asyncio

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
rp0Angle = 0.0
rp0Distance = 0.0
rp1Angle = 0.0
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
    def __init__(self, ):
        self.numLoops = 0

    async def com_disconnect(self):
        await asyncio.sleep(0.01)
        Disconnecting_task_0 = loop.create_task(RaspberryPi0.Disconnecting())
        Disconnecting_task_1 = loop.create_task(RaspberryPi1.Disconnecting())
        await asyncio.wait([Disconnecting_task_0, Disconnecting_task_1, ])
        await self.com_undock()
        self.numLoops = numLoops +1
        

    async def com_dock(self):
        await asyncio.sleep(0.01)
        await self.com_disconnect()

    async def com_turn5(self):
        await asyncio.sleep(0.01)
        Turning5_task_0 = loop.create_task(RaspberryPi0.Turning5())
        Turning5_task_1 = loop.create_task(RaspberryPi1.Turning5())
        await asyncio.wait([Turning5_task_0, Turning5_task_1, ])
        await self.com_dock()
        rp0Angle = -90.0
        rp1Angle = 90.0
        

    async def com_map2(self):
        await asyncio.sleep(0.01)
        await self.com_turn5()
        map2Rp0 = numLoops +1
        map2Rp1 = numLoops +1
        

    async def com_scan2(self):
        await asyncio.sleep(0.01)
        Scanning2_task_0 = loop.create_task(RaspberryPi0.Scanning2())
        Scanning2_task_1 = loop.create_task(RaspberryPi1.Scanning2())
        await asyncio.wait([Scanning2_task_0, Scanning2_task_1, ])
        await self.com_map2()
        rp0ScanTime = 2.0
        rp1ScanTime = 2.0
        

    async def com_move4(self):
        await asyncio.sleep(0.01)
        await self.com_scan2()
        rp0Distance = 1.0
        rp1Distance = 1.0
        

    async def com_turn4(self):
        await asyncio.sleep(0.01)
        Turning4_task_0 = loop.create_task(RaspberryPi0.Turning4())
        Turning4_task_1 = loop.create_task(RaspberryPi1.Turning4())
        await asyncio.wait([Turning4_task_0, Turning4_task_1, ])
        await self.com_move4()
        rp0Angle = 90.0
        rp1Angle = -90.0
        

    async def com_move3(self):
        await asyncio.sleep(0.01)
        await self.com_turn4()
        rp0Distance = 1.0
        rp1Distance = 1.0
        

    async def com_map1(self):
        await asyncio.sleep(0.01)
        Mapping1_task_0 = loop.create_task(RaspberryPi0.Mapping1())
        Mapping1_task_1 = loop.create_task(RaspberryPi1.Mapping1())
        await asyncio.wait([Mapping1_task_0, Mapping1_task_1, ])
        await self.com_move3()
        map1Rp0 = numLoops +1
        map1Rp1 = numLoops +1
        

    async def com_scan1(self):
        await asyncio.sleep(0.01)
        await self.com_map1()
        rp0ScanTime = 1.0
        rp1ScanTime = 1.0
        

    async def com_turn3(self):
        await asyncio.sleep(0.01)
        Turning3_task_0 = loop.create_task(RaspberryPi0.Turning3())
        Turning3_task_1 = loop.create_task(RaspberryPi1.Turning3())
        await asyncio.wait([Turning3_task_0, Turning3_task_1, ])
        await self.com_scan1()
        rp0Angle = 90.0
        rp1Angle = -90.0
        

    async def com_move2(self):
        await asyncio.sleep(0.01)
        await self.com_turn3()
        rp0Distance = 1.0
        rp1Distance = 1.0
        

    async def com_turn2(self):
        await asyncio.sleep(0.01)
        Turning2_task_0 = loop.create_task(RaspberryPi0.Turning2())
        Turning2_task_1 = loop.create_task(RaspberryPi1.Turning2())
        await asyncio.wait([Turning2_task_0, Turning2_task_1, ])
        await self.com_move2()
        rp0Angle = 90.0
        rp1Angle = -90.0
        

    async def com_move1(self):
        await asyncio.sleep(0.01)
        await self.com_turn2()
        rp0Distance = 1.0
        rp1Distance = 1.0
        

    async def com_turn1(self):
        await asyncio.sleep(0.01)
        Turning1_task_0 = loop.create_task(RaspberryPi0.Turning1())
        Turning1_task_1 = loop.create_task(RaspberryPi1.Turning1())
        await asyncio.wait([Turning1_task_0, Turning1_task_1, ])
        await self.com_move1()
        rp0Angle = 180.0
        rp1Angle = -180.0
        

    async def com_undock(self):
        await asyncio.sleep(0.01)
        await self.com_turn1()
        rp0Distance = -0.1
        rp1Distance = -0.1
        

    async def com_init(self):
        await asyncio.sleep(0.01)
        Initalized_task_0 = loop.create_task(RaspberryPi0.Initalized())
        Initalized_task_1 = loop.create_task(RaspberryPi1.Initalized())
        await asyncio.wait([Initalized_task_0, Initalized_task_1, ])
        await self.com_undock()

class RaspberryPi0:
    def __init__(self, ):
        self.piNum = 0

    async def Disconnecting(self):
        await asyncio.sleep(0.01)
        await self.Undock()

    async def Docking(self):
        await asyncio.sleep(0.01)
        com_dock_task_0 = loop.create_task(CentralController.com_dock())
        await asyncio.wait([com_dock_task_0, ])
        await self.Disconnecting()

    async def Turning5(self):
        await asyncio.sleep(0.01)
        await self.Docking()

    async def Mapping2(self):
        await asyncio.sleep(0.01)
        com_map2_task_0 = loop.create_task(CentralController.com_map2())
        await asyncio.wait([com_map2_task_0, ])
        await self.Turning5()

    async def Scanning2(self):
        await asyncio.sleep(0.01)
        await self.Mapping2()

    async def Moving4(self):
        await asyncio.sleep(0.01)
        com_move4_task_0 = loop.create_task(CentralController.com_move4())
        await asyncio.wait([com_move4_task_0, ])
        await self.Scanning2()

    async def Turning4(self):
        await asyncio.sleep(0.01)
        await self.Moving4()

    async def Moving3(self):
        await asyncio.sleep(0.01)
        com_move3_task_0 = loop.create_task(CentralController.com_move3())
        await asyncio.wait([com_move3_task_0, ])
        await self.Turning4()

    async def Mapping1(self):
        await asyncio.sleep(0.01)
        await self.Moving3()

    async def Scanning1(self):
        await asyncio.sleep(0.01)
        com_scan1_task_0 = loop.create_task(CentralController.com_scan1())
        await asyncio.wait([com_scan1_task_0, ])
        await self.Mapping1()

    async def Turning3(self):
        await asyncio.sleep(0.01)
        await self.Scanning1()

    async def Moving2(self):
        await asyncio.sleep(0.01)
        com_move2_task_0 = loop.create_task(CentralController.com_move2())
        await asyncio.wait([com_move2_task_0, ])
        await self.Turning3()

    async def Turning2(self):
        await asyncio.sleep(0.01)
        await self.Moving2()

    async def Moving1(self):
        await asyncio.sleep(0.01)
        com_move1_task_0 = loop.create_task(CentralController.com_move1())
        await asyncio.wait([com_move1_task_0, ])
        await self.Turning2()

    async def Turning1(self):
        await asyncio.sleep(0.01)
        await self.Moving1()

    async def Undock(self):
        await asyncio.sleep(0.01)
        com_undock_task_0 = loop.create_task(CentralController.com_undock())
        await asyncio.wait([com_undock_task_0, ])
        await self.Turning1()

    async def Initalized(self):
        await asyncio.sleep(0.01)
        await self.Undock()

class RaspberryPi1:
    def __init__(self, ):
        self.piNum = 1

    async def Disconnecting(self):
        await asyncio.sleep(0.01)
        await self.Undock()

    async def Docking(self):
        await asyncio.sleep(0.01)
        com_dock_task_0 = loop.create_task(CentralController.com_dock())
        await asyncio.wait([com_dock_task_0, ])
        await self.Disconnecting()

    async def Turning5(self):
        await asyncio.sleep(0.01)
        await self.Docking()

    async def Mapping2(self):
        await asyncio.sleep(0.01)
        com_map2_task_0 = loop.create_task(CentralController.com_map2())
        await asyncio.wait([com_map2_task_0, ])
        await self.Turning5()

    async def Scanning2(self):
        await asyncio.sleep(0.01)
        await self.Mapping2()

    async def Moving4(self):
        await asyncio.sleep(0.01)
        com_move4_task_0 = loop.create_task(CentralController.com_move4())
        await asyncio.wait([com_move4_task_0, ])
        await self.Scanning2()

    async def Turning4(self):
        await asyncio.sleep(0.01)
        await self.Moving4()

    async def Moving3(self):
        await asyncio.sleep(0.01)
        com_move3_task_0 = loop.create_task(CentralController.com_move3())
        await asyncio.wait([com_move3_task_0, ])
        await self.Turning4()

    async def Mapping1(self):
        await asyncio.sleep(0.01)
        await self.Moving3()

    async def Scanning1(self):
        await asyncio.sleep(0.01)
        com_scan1_task_0 = loop.create_task(CentralController.com_scan1())
        await asyncio.wait([com_scan1_task_0, ])
        await self.Mapping1()

    async def Turning3(self):
        await asyncio.sleep(0.01)
        await self.Scanning1()

    async def Moving2(self):
        await asyncio.sleep(0.01)
        com_move2_task_0 = loop.create_task(CentralController.com_move2())
        await asyncio.wait([com_move2_task_0, ])
        await self.Turning3()

    async def Turning2(self):
        await asyncio.sleep(0.01)
        await self.Moving2()

    async def Moving1(self):
        await asyncio.sleep(0.01)
        com_move1_task_0 = loop.create_task(CentralController.com_move1())
        await asyncio.wait([com_move1_task_0, ])
        await self.Turning2()

    async def Turning1(self):
        await asyncio.sleep(0.01)
        await self.Moving1()

    async def Undock(self):
        await asyncio.sleep(0.01)
        com_undock_task_0 = loop.create_task(CentralController.com_undock())
        await asyncio.wait([com_undock_task_0, ])
        await self.Turning1()

    async def Initalized(self):
        await asyncio.sleep(0.01)
        await self.Undock()

loop = asyncio.get_event_loop()
Pi0 = RaspberryPi0()
Pi1 = RaspberryPi1()
CC = CentralController()
loop.run_until_complete(CC.com_init())
loop.run_until_complete(Pi0.Initalized())
loop.run_until_complete(Pi1.Initalized())