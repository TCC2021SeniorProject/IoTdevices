'''Written by Cael Shoop. To be combined with translator output.'''

import time
import piInterface as piI


def com_init(self):
    piI.Connect()


def com_connect(self):
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


def Dancing1(self, piNum):
    piout = piI.Shell('dance1', piNum)
    while 'danced1' not in piout:
        time.sleep(1)
        piout = piI.Shell('', piNum)


def Dancing2(self, piNum):
    piout = piI.Shell('dance2', piNum)
    while 'danced2' not in piout:
        time.sleep(1)
        piout = piI.Shell('', piNum)


def com_dock(self, piNum): # or "Docking()" ???
    piout = piI.Shell('dock', piNum)
    while 'docked' not in piout:
        time.sleep(1)
        piout = piI.Shell('', piNum)


def com_disconnect(self): # or "Disconnecting()" ???
    piout = piI.ShellBoth('disconnect')
    while 'disconnected' not in piout:
        time.sleep(1)
        piout = piI.ShellBoth('')
    piI.Disconnect()
    time.sleep(3)