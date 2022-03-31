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
            Pi0.Disconnecting()
            Pi1.Disconnecting()
            await self.com_init()

    async def com_dock(self):
        if self.request == 2:
            await self.com_disconnect()

    async def com_dance(self):
        if self.request == 1:
            Pi0.Dancing0()
            Pi1.Dancing1()
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
        #Pi0.Idle()
        Pi1.Idle()
        await self.com_init()
    
    def between_idle(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(Pi0.Idle())
        loop.close()

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
        self.request = 0
        
        await self.Initalized()

    async def Docking(self):
        piout = piI.Shell('dock', self.piNum)
        while 'docked' not in piout:
            time.sleep(1)
            piout = piI.Shell('', self.piNum)
        self.request = 3
        
        Laptop.com_dock()
        await self.Disconnecting()

    async def Dancing0(self):
        piout = piI.Shell('dance0', self.piNum)
        while 'danced0' not in piout:
            time.sleep(1)
            piout = piI.Shell('', self.piNum)
        self.request = 2
        
        await self.Docking()

    async def Initalized(self):
        self.request = 1
        
        Laptop.com_init()
        await self.Dancing0()

    async def Idle(self):
        print('Pi0 Idle')
        self.request = 0
        
        await self.Initalized()

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
        self.request = 0
        
        await self.Initalized()

    async def Docking(self):
        piout = piI.Shell('dock', self.piNum)
        while 'docked' not in piout:
            time.sleep(1)
            piout = piI.Shell('', self.piNum)
        self.request = 3
        
        Laptop.com_dock()
        await self.Disconnecting()

    async def Dancing1(self):
        piout = piI.Shell('dance1', self.piNum)
        while 'danced1' not in piout:
            time.sleep(1)
            piout = piI.Shell('', self.piNum)
        self.request = 2
        
        await self.Docking()

    async def Initalized(self):
        self.request = 1
        
        Laptop.com_init()
        await self.Dancing1()

    async def Idle(self):
        self.request = 0
        
        await self.Initalized()

loop = asyncio.get_event_loop()
Pi0 = RasPi0(connection, initalize, dance, dock, disconnect, request)
Pi1 = RasPi1(connection, initalize, dance, dock, disconnect, request)
Laptop = MCCD(connection, initalize, dance, dock, disconnect, request, Pi0, Pi1, )
_thread = threading.Thread(target=Laptop.between_idle, args=(''))
_thread.start()
#loop.run_until_complete(Laptop.com_connect())
#loop.run_until_complete(Pi0.Idle())
#loop.run_until_complete(Pi1.Idle())
