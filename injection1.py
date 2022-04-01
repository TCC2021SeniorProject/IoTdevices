'''Written by Cael Shoop. To be combined with translator output.'''

import time
import piInterface as piI


def com_init(self):
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


def Dancing0(self):
    piout = piI.Shell('dance0', self.piNum)
    while 'danced0' not in piout:
        time.sleep(1)
        piout = piI.Shell('', self.piNum)


def Dancing1(self):
    piout = piI.Shell('dance1', self.piNum)
    while 'danced1' not in piout:
        time.sleep(1)
        piout = piI.Shell('', self.piNum)


def Docking(self):
    piout = piI.Shell('dock', self.piNum)
    while 'docked' not in piout:
        time.sleep(1)
        piout = piI.Shell('', self.piNum)


def com_disconnect(self):
    pi0, pi1 = piI.ShellBoth('disconnect')
    while 'disconnected' not in pi0:
        time.sleep(1)
        pi0 = piI.Shell('', 0)
    while 'disconnected' not in pi1:
        time.sleep(1)
        pi1 = piI.Shell('', 1)
    piI.Disconnect()
    time.sleep(3)