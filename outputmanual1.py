import asyncio
import threading
import time
import piInterface as piI

connection = None #Channel variable
initalize = None #Channel variable
dance = None #Channel variable
disconnect = None #Channel variable
dock = None #Channel variable
request = 0

class MCCD:
    def __init__(self, connection, initalize, dance, dock, disconnect, request, Pi0, Pi1, ):
        self.connection = connection
        self.initalize = initalize
        self.dance = dance
        self.dock = dock
        self.disconnect = disconnect
        self.request = request

    async def com_disconnect(self):
        pi0, pi1 = piI.ShellBoth('disconnect')
        while 'disconnected' not in pi0:
            time.sleep(1)
            pi0 = piI.Shell('', 0)
        while 'disconnected' not in pi1:
            time.sleep(1)
            pi1 = piI.Shell('', 1)
        piI.Disconnect()
        time.sleep(3)
        if self.request == 3:
            pi0Dis = loop.create_task(Pi0.Disconnecting())
            pi1Dis = loop.create_task(Pi1.Disconnecting())
            await asyncio.wait([pi0Dis, pi1Dis])
            await self.com_init()

    async def com_dock(self):
        if self.request == 2:
            await self.com_disconnect()

    async def com_dance(self):
        if self.request == 1:
            pi0Dan = loop.create_task(Pi0.Dancing0())
            pi1Dan = loop.create_task(Pi1.Dancing1())
            await asyncio.wait([pi0Dan, pi1Dan])
            await self.com_dock()

    async def com_init(self):
        piI.Connect()
        pi0, pi1 = piI.ShellBoth('python3 -i predefined1.py\n')
        print(str(pi0) + '\n' + str(pi1))
        while 'connected' not in pi0:
            time.sleep(1)
            pi0 = piI.Shell('', 0)
            print(pi0)
        while 'connected' not in pi1:
            time.sleep(1)
            pi1 = piI.Shell('', 1)
            print(pi1)
        if self.request == 0:
            await self.com_dance()

    async def com_connect(self):
        pi0Idl = loop.create_task(Pi0.Idle())
        pi1Idl = loop.create_task(Pi1.Idle())
        await asyncio.wait([pi0Idl, pi1Idl])
        await self.com_init()
    
class RasPi0:
    def __init__(self, connection, initalize, dance, dock, disconnect, request, ):
        self.connection = connection
        self.initalize = initalize
        self.dance = dance
        self.dock = dock
        self.disconnect = disconnect
        self.request = request
        self.piNum = 0

    async def Disconnecting(self):
        await asyncio.sleep(.01)
        self.request = 0
        
        await self.Initialized()

    async def Docking(self):
        piout = piI.Shell('dock', self.piNum)
        while 'docked' not in piout:
            time.sleep(1)
            piout = piI.Shell('', self.piNum)
        self.request = 3
        
        await Laptop.com_dock()
        await self.Disconnecting()

    async def Dancing0(self):
        piout = piI.Shell('dance0', self.piNum)
        while 'danced0' not in piout:
            time.sleep(1)
            piout = piI.Shell('', self.piNum)
        self.request = 2
        
        await self.Docking()

    async def Initialized(self):
        self.request = 1
        
        await Laptop.com_init()
        await self.Dancing0()

    async def Idle(self):
        await asyncio.sleep(.01)
        self.request = 0
        
        await self.Initialized()

class RasPi1:
    def __init__(self, connection, initalize, dance, dock, disconnect, request, ):
        self.connection = connection
        self.initalize = initalize
        self.dance = dance
        self.dock = dock
        self.disconnect = disconnect
        self.request = request
        self.piNum = 1

    async def Disconnecting(self):
        await asyncio.sleep(.01)
        self.request = 0
        
        await self.Initialized()

    async def Docking(self):
        piout = piI.Shell('dock', self.piNum)
        while 'docked' not in piout:
            time.sleep(1)
            piout = piI.Shell('', self.piNum)
        self.request = 3
        
        await Laptop.com_dock()
        await self.Disconnecting()

    async def Dancing1(self):
        piout = piI.Shell('dance1', self.piNum)
        while 'danced1' not in piout:
            time.sleep(1)
            piout = piI.Shell('', self.piNum)
        self.request = 2
        
        await self.Docking()

    async def Initialized(self):
        self.request = 1
        
        await Laptop.com_init()
        await self.Dancing1()

    async def Idle(self):
        await asyncio.sleep(.01)
        self.request = 0
        
        await self.Initialized()

loop = asyncio.get_event_loop()
Pi0 = RasPi0(connection, initalize, dance, dock, disconnect, request)
Pi1 = RasPi1(connection, initalize, dance, dock, disconnect, request)
Laptop = MCCD(connection, initalize, dance, dock, disconnect, request, Pi0, Pi1, )
loop.run_until_complete(Laptop.com_connect())
loop.run_until_complete(Pi0.Idle())
loop.run_until_complete(Pi1.Idle())
loop.close()