import asyncio
import time
from pycreate2 import Create2
import piInterface as piI

direct1 = 0
direct2 = 0
request1 = 0
request2 = 0

class roomba:
    def __init__(self, request, mode, ):
        self.request = request
        self.mode = mode

    async def Dancing(self):
        if self.mode == 1:
            await self.Initialized()

    async def Waiting(self):
        if self.mode == 3:
            await self.Dancing()

    async def Initialized(self):
        if self.mode == 2:
            await self.Waiting()

    async def Idle(self):
        if self.mode == 1:
            await self.Initialized()

class MCCD:
    def __init__(self, req1, mode1, req2, mode2, ):
        self.req1 = req1
        self.req2 = req2
        self.mode1 = mode1
        self.mode2 = mode2
    
    async def done(self):
        piI.TransferBoth('two.txt')
        time.sleep(2)
        piI.SendBoth('rm zero.txt')
        piI.SendBoth('rm one.txt')
        piI.SendBoth('rm two.txt')
        piI.Disconnect()

    async def com_dock(self, piNum):
        piI.Transfer('one.txt', piNum)
        time.sleep(2)
        if self.mode1 == 2 and self.mode2 == 2:
            await self.done()

    async def dancing1(self):
        piI.Transfer('zero.txt', 0)
        self.mode1 = 2
        time.sleep(8)
        await self.com_dock(0)

    async def dancing2(self):
        piI.Transfer('zero.txt', 1)
        self.mode2 = 2
        time.sleep(8)
        await self.com_dock(1)

    async def com_dance(self):
        time.sleep(2)
        await self.dancing1()
        if self.mode1 == 2:
            await self.dancing2()

    async def check_init(self):
        if self.req1 == 0 and self.mode1 == 1:
            await self.com_dance()

    async def com_init(self):
        global ssh
        ssh = piI.Connect()
        if not ssh:
            print('Error. Exiting.')
            exit()
        piI.SendBoth('python3 predefined2.py')
        time.sleep(1)
        self.mode1 = 1
        self.mode2 = 1
        
        await self.check_init()

loop = asyncio.get_event_loop()
Laptop = MCCD(request1, direct1, request2, direct2)
Roomba1 = roomba(request1, direct1)
Roomba2 = roomba(request2, direct2)
loop.run_until_complete(Laptop.com_init())
