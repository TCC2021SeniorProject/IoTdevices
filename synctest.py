import time
import asyncio

class CentralController:
    def __init__(self, Pi0, Pi1):
        self.numLoops = 0
        self.Pi0 = Pi0
        self.Pi1 = Pi1
    
    async def test(self):
        print('test()')

        loop2 = asyncio.get_event_loop()
        test0 = loop2.create_task(self.Pi0.test())
        test1 = loop2.create_task(self.Pi1.test())
        await asyncio.wait([test0, test1])
        #await asyncio.gather(self.Pi0.test(), self.Pi1.test())

class RaspPi0:
    def __init__(self):
        self.piNum = 0
    
    async def test(self):
        await asyncio.sleep(0.01)
        print('Pi0 test()')
        await asyncio.sleep(0.01)
        print('Pi0 test(1)')
        await asyncio.sleep(0.01)
        print('Pi0 test(2)')

class RaspPi1:
    def __init__(self):
        self.piNum = 0
    
    async def test(self):
        await asyncio.sleep(0.01)
        print('Pi1 test()')
        await asyncio.sleep(0.01)
        print('Pi1 test(1)')
        await asyncio.sleep(0.01)
        print('Pi1 test(2)')

loop = asyncio.get_event_loop()
Pi0 = RaspPi0()
Pi1 = RaspPi1()
cc = CentralController(Pi0, Pi1)
try:
    loop.run_until_complete(cc.test())
    loop.run_until_complete(loop.shutdown_asyncgens())
finally:
    loop.close()