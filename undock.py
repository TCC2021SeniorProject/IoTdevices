import piInterface as piI
import time
import sys


piI.Connect()
if len(sys.argv) > 1:
    if len(sys.argv[1] == 0):
        out = piI.Shell('python3 undockpredef.py\n', 0)
        print(str(out), end='')
        while 'undocked' not in out:
            time.sleep(.1)
            out = piI.Shell('', 0)
            print(out, end='')
    else:
        out = piI.Shell('python3 undockpredef.py\n', 1)
        print(str(out), end='')
        while 'undocked' not in out:
            time.sleep(.1)
            out = piI.Shell('', 1)
            print(out, end='')
else:
    pi0, pi1 = piI.ShellBoth('python3 undockpredef.py\n')
    print(str(pi0) + str(pi1), end='')
    while 'undocked' not in pi0:
        time.sleep(.1)
        pi0 = piI.Shell('', 0)
        print(pi0, end='')
    while 'undocked' not in pi1:
        time.sleep(.1)
        pi1 = piI.Shell('', 1)
        print(pi1, end='')
piI.Disconnect()