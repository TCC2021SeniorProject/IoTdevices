from pycreate2 import Create2
import time

try:
    bot = Create2('/dev/ttyUSB0')
except:
    bot = Create2('/dev/ttyUSB1')
bot.start()
bot.safe()

bot.drive_direct(-300, -300)
time.sleep(.5)
bot.drive_stop()

bot.close()
print('undocked')