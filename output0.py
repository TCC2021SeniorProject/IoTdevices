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
        print('In done')
        pi0, pi1 = piI.ShellBoth('\n')
        print(pi0)
        print(pi1)
        while 'Finish' not in pi0 or 'Finish' not in pi1:
            time.sleep(1)
            pi0, pi1 = piI.ShellBoth('')
            print(pi0)
            print(pi1)
        piI.Disconnect()

    async def com_dock(self, piNum):
        print('In com_dock')
        output = piI.Shell('\n', piNum)
        while 'Dock' not in output:
            time.sleep(1)
            output = piI.Shell('')
            print(output)
        if self.mode1 == 2 and self.mode2 == 2:
            await self.done()

    async def dancing1(self):
        print('In dancing1')
        output = piI.Shell('\n', 0)
        while 'Dance' not in output:
            time.sleep(1)
            output = piI.Shell('', 0)
            print(output)
        self.mode1 = 2
        await self.com_dock(0)

    async def dancing2(self):
        print('In dancing2')
        output = piI.Shell('\n', 1)
        while 'Dance' not in output:
            time.sleep(1)
            output = piI.Shell('', 1)
            print(output)
        self.mode2 = 2
        await self.com_dock(1)

    async def com_dance(self):
        print('In com_dance')
        await self.dancing1()
        if self.mode1 == 2:
            await self.dancing2()

    async def check_init(self):
        print('In check_init')
        if self.req1 == 0 and self.mode1 == 1:
            await self.com_dance()

    async def com_init(self):
        print('In com_init')
        global ssh
        piI.Connect()
        pi0, pi1 = piI.ShellBoth('python3 -i predefined0.py\n')
        print(str(pi0))
        print(str(pi1))
        self.mode1 = 1
        self.mode2 = 1
        
        await self.check_init()

loop = asyncio.get_event_loop()
Laptop = MCCD(request1, direct1, request2, direct2)
Roomba1 = roomba(request1, direct1)
Roomba2 = roomba(request2, direct2)
loop.run_until_complete(Laptop.com_init())
