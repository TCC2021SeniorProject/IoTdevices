import asyncio

connection = None #Channel variable
initalize = None #Channel variable
dance = None #Channel variable
disconnect = None #Channel variable
dock = None #Channel variable
request = 0

class MCCD:
    def __init__(self, connection, initalize, dance, dock, disconnect, request, ):
        self.connection = connection
        self.initalize = initalize
        self.dance = dance
        self.dock = dock
        self.disconnect = disconnect
        self.request = request

    async def com_disconnect(self):
        if self.request == 3:
            RasPi1.Disconnecting()
            RasPi2.Disconnecting()
            await self.com_init()

    async def com_dock(self):
        if self.request == 2:
            await self.com_disconnect()

    async def com_dance(self):
        if self.request == 1:
            RasPi1.Dancing1()
            RasPi2.Dancing2()
            await self.com_dock()

    async def com_init(self):
        if self.request == 0:
            await self.com_dance()

    async def com_connect(self):
        RasPi1.Idle()
        RasPi2.Idle()
        await self.com_init()

class RasPi1:
    def __init__(self, connection, initalize, dance, dock, disconnect, request, ):
        self.connection = connection
        self.initalize = initalize
        self.dance = dance
        self.dock = dock
        self.disconnect = disconnect
        self.request = request

    async def Disconnecting(self):
        self.request = 0
        
        await self.Initalized()

    async def Docking(self):
        self.request = 3
        
        MCCD.com_dock()
        await self.Disconnecting()

    async def Dancing1(self):
        self.request = 2
        
        await self.Docking()

    async def Initalized(self):
        self.request = 1
        
        MCCD.com_init()
        await self.Dancing1()

    async def Idle(self):
        self.request = 0
        
        await self.Initalized()

class RasPi2:
    def __init__(self, connection, initalize, dance, dock, disconnect, request, ):
        self.connection = connection
        self.initalize = initalize
        self.dance = dance
        self.dock = dock
        self.disconnect = disconnect
        self.request = request

    async def Disconnecting(self):
        self.request = 0
        
        await self.Initalized()

    async def Docking(self):
        self.request = 3
        
        MCCD.com_dock()
        await self.Disconnecting()

    async def Dancing2(self):
        self.request = 2
        
        await self.Docking()

    async def Initalized(self):
        self.request = 1
        
        MCCD.com_init()
        await self.Dancing2()

    async def Idle(self):
        self.request = 0
        
        await self.Initalized()

loop = asyncio.get_event_loop()
Laptop = MCCD(connection, initalize, dance, dock, disconnect, request)
Pi1 = RasPi1(connection, initalize, dance, dock, disconnect, request)
Pi2 = RasPi2(connection, initalize, dance, dock, disconnect, request)
loop.run_until_complete(Laptop.com_connect())
loop.run_until_complete(Pi1.Idle())
loop.run_until_complete(Pi2.Idle())
