import asyncio

RoombaConnect = None #Channel variable
wait = True
wait2 = True

class MCCD:
    def __init__(self, ):
        pass

    async def close(self):
        exit()

    async def wait_process(self):
        if self.wait == False:
            await self.close()

    async def Initialize(self):
        roomba.Connect()
        await self.wait_process()

class Roomba_Instance1:
    def __init__(self, ):
        pass

    async def Dock(self):
        exit()

    async def GoFront(self):
        self.wait = False
        await self.Dock()

    async def Ready(self):
        await self.GoFront()

    async def Connect(self):
        await self.Ready()

    async def default_init(self):
        await self.Connect()

loop = asyncio.get_event_loop()
mccd = MCCD()
roomba = Roomba_Instance1()
loop.run_until_complete(mccd.Initialize())