'''This script is meant to send directions to the Roombas. Written by Cael Shoop.'''

import args


# Drive Modes:
# 0: Drive (default)
# 1: DriveDirect
# 2: DrivePWM

# Directions:
# 0: Forward (default)
# 1: Backward
# 2: Rotate CW
# 3: Rotate CCW

# Speeds:
# 0-100 (%) (100 default)

# Safe Mode:
# True: Safe (default)
# False: Full

def getSerialData(safe, driveMode, speed, direction):
    if not direction:
        print('Fatal error: No direction provided to roombaDirect.py. Exiting.')
        exit()
    if not speed:
        speed = 100
    if not driveMode:
        driveMode = 0
    if not safe:
        safe = True

    data = '80'

    if safe == True:
        data += '83'
    else:
        data += '84'

    if driveMode == 0:
        data += '89'
        if direction == 0 and speed == 100:
            data += '8000'
        elif direction == 0:
            data += ''
            print('<<< FEATURE PENDING >>>')
        elif direction == 1 and speed == 100:
            data += '7fff'
        elif direction == 1:
            data += ''
            print('<<< FEATURE PENDING >>>')
        elif direction == 2:
            data += 'ffff'
        elif direction == 3:
            data += '0001'
    elif driveMode == 1:
        data += '91'
    elif driveMode == 2:
        data += '92'
    else:
        print('Fatal error: Invalid DRIVE MODE provided to roombaDirect.py. Exiting.')
        exit()

    if direction == 0:
        print('<<< FEATURE PENDING >>>')
    elif direction == 1:
        print('<<< FEATURE PENDING >>>')
    elif direction == 2:
        print('<<< FEATURE PENDING >>>')
    elif direction == 3:
        print('<<< FEATURE PENDING >>>')
    else:
        print('Fatal error: Invalid DIRECTION provided to roombaDirect.py. Exiting.')
        exit()
    
    if speed == 0:
        print('<<< FEATURE PENDING >>>')
    elif 100 > speed > 0:
        print('<<< FEATURE PENDING >>>')
    elif speed == 100:
        print('<<< FEATURE PENDING >>>')
    else:
        print('Fatal error: Invalid SPEED provided to roombaDirect.py. Exiting.')
        exit()

    data += 'ad'


    ###-------- Movement Data ----------------
    ### Basics
    # data_start = '80'                   # Data to start OI
    # data_safe = '83'                    # Data for safe mode
    # data_full = '84'                    # Data for full mode
    # data_clean = '87'                   # Data for clean
    # data_dock = '8f'                    # Data for dock
    # data_halt = '9100000000'            # Data to stop Roomba movement
    # data_stop = 'ad'                    # Data to stop OI
    ### Drive
    # data_forward_full = '898000'        # Data for full speed forward motion
    # data_forward_half = '8900fa0000'    # Data for half speed forward motion
    # data_rotate_cw = '89ffff'           # Data to spin clockwise
    # data_rotate_ccw = '890001'          # Data to spin counter-clockwise
    # data_backward_full = '897fff'       # Data for full speed backward motion
    # data_backward_half = '89ff060000'   # Data for half speed backward motion
    ### Drive Direct
    # data_dd_forward_full = '9101f401f4'
    # data_dd_forward_half = '9100ff00ff'
    # data_dd_rotate_cw = '91fe0c01f4'
    # data_dd_rotate_ccw = '9101f4fe0c'
    # data_dd_backward_full = '91fe0cfe0c'
    # data_dd_backward_half = '91ff01ff01'
    ### Drive PWM
    # data_pwm_forward_full = '9200ff00ff'
    # data_pwm_forward_half = '9200880088'
    # data_pwm_rotate_cw = '92ff0100ff'
    # data_pwm_rotate_ccw = '9200ffff01'
    # data_pwm_backward_full = '92ff01ff01'
    # data_pwm_backward_half = '9288018801'


    args.parseargs()