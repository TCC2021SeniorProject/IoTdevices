from pprint import pformat
#import json
import socket
#import serial
import ssl
import sys
import time
from ast import literal_eval

def send(addr, data):
    # Send MQTT magic packet to addr
    # This is 0xf0 (mqtt reserved) 0x05(data length) 0x91???????? (data)
    # Should tell Roomba to move forward at full speed.
    # Uses 10 second timeout for socket connection
    packet = bytes.fromhex(data)
    #packet = serial.to_bytes(data)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(10)

    #context = ssl.SSLContext(ssl.PROTOCOL_TLS)
    context = ssl.SSLContext()
    context.set_ciphers('DEFAULT@SECLEVEL=2:HIGH:!DH:!aNULL')
    wrappedSocket = context.wrap_socket(sock)

    no_error = True
    try:
        wrappedSocket.connect((addr, 8883))
        print('Connection successful.')
        wrappedSocket.send(packet)
        print('Command sent.')
        wrappedSocket.close()
        return no_error
    except socket.timeout as e:
        no_error = False
        print('Connection Timeout Error (for {}): {}'.format(addr, e))
    except (ConnectionRefusedError, OSError) as e:
        no_error = False
        if e.errno == 111:      #errno.ECONNREFUSED
            print('Unable to Connect to roomba at ip {}, make sure nothing else is connected (app?), '
                            'as only one connection at a time is allowed'.format(addr))
        elif e.errno == 113:    #errno.No Route to Host
            print('Unable to contact roomba on ip {}, is the ip correct?'.format(addr))
        else:
            print("Connection Error (for {}): {}".format(addr, e))
    except Exception as e:
        no_error = False
        print(e)
    return no_error


def main():
    import argparse
    
    #-------- Command Line -----------------
    parser = argparse.ArgumentParser(
        description='Forward MQTT data to Roomba for directional control.')
    parser.add_argument(
        '-o','--oneroomba',
        action='store',
        type=str,
        default='2',
        help='Choose a Roomba. \'0\' (Roomba0), \'1\' (Roomba1), or \'2\' (Both).')
    parser.add_argument(
        '-d','--direction',
        action='store',
        type=str,
        default='backward',
        help='Choose a direction. \'forward\', \'forwardhalf\', \'rotatecw\', \'rotateccw\', \'backward\', \'backwardhalf\'')
    parser.add_argument(
        '-s','--safemode',
        action='store',
        type=str,
        default='safe',
        help='Choose safe mode or full mode. Default is safe. \'safe\' or \'full\'.')
    parser.add_argument(
        '-m','--drive',
        action='store',
        type=str,
        default='drive',
        help='Choose a drive mode. \'drive\', \'dd\', or \'pwm\'.')
    arg = parser.parse_args()

    #-------- Movement Data ----------------
    data_start = 'f00180'                   # Data to start OI
    #data_start = [0xf0, 0x01, 0x80]
    data_safe = 'f00183'                    # Data for safe mode
    #data_safe = [0xf0, 0x01, 0x83]
    data_full = 'f00184'                    # Data for full mode
    # Drive
    data_forward_full = 'f003898000'        # Data for full speed forward motion
    data_forward_half = 'f003894000'        # Data for half speed forward motion
    data_rotate_cw = 'f00389ffff'           # Data to spin clockwise
    data_rotate_ccw = 'f003890001'          # Data to spin counter-clockwise
    data_backward_full = 'f003897fff'       # Data for full speed backward motion
    data_backward_half = 'f00389bfff'      # Data for half speed backward motion
    # Drive Direct
    data_dd_forward_full = 'f0059101f401f4'
    data_dd_forward_half = 'f0059100ff00ff'
    data_dd_rotate_cw = 'f00591fe0c01f4'
    #data_dd_rotate_cw = [0xf0, 0x05, 0x91, 0xfe, 0x0c, 0x01, 0xf4]
    data_dd_rotate_ccw = 'f0059101f4fe0c'
    data_dd_backward_full = 'f00591fe0cfe0c'
    data_dd_backward_half = 'f00591ff01ff01'
    # Drive PWM
    data_pwm_forward_full = 'f0059200ff00ff'
    #data_pwm_forward_half = ''
    data_pwm_rotate_cw = 'f00592ff0100ff'
    data_pwm_rotate_ccw = 'f0059200ffff01'
    data_pwm_backward_full = 'f00592ff01ff01'
    #data_pwm_backward_half = ''
    data_halt = 'f0059100000000'                # Data to stop Roomba movement
    #data_halt = [0xf0, 0x05, 0x89, 0x00, 0x00, 0x00, 0x00]
    data_stop = 'f001ad'                    # Data to stop OI
    #data_stop = [0xf0, 0x01, 0xad]
    
    if arg.oneroomba == '0':
        roomba = '192.168.1.33'
    elif arg.oneroomba == '1':
        roomba = '192.168.1.38'
    elif arg.oneroomba == '2':
        roomba = 'both'
    else:
        print('Invalid Roomba selection.')

    if arg.drive == 'drive':
        print('Drive selected.')
        if arg.direction == 'forward':
            print('Forward selected.')
            data = data_forward_full
        elif arg.direction == 'forwardhalf':
            print('Half speed forward selected.')
            data = data_forward_half
        elif arg.direction == 'rotatecw':
            print('Rotate Clockwise selected.')
            data = data_rotate_cw
        elif arg.direction == 'rotateccw':
            print('Rotate Counterclockwise selected.')
            data = data_rotate_ccw
        elif arg.direction == 'backward':
            print('Backward selected.')
            data = data_backward_full
        elif arg.direction == 'backwardhalf':
            print('Half speed backward selected.')
            data = data_backward_half
        else:
            print('Invalid Roomba direction.')
            return
    elif arg.drive == 'dd':
        print('Drive Direct selected.')
        if arg.direction == 'forward':
            print('Forward selected.')
            data = data_dd_forward_full
        elif arg.direction == 'forwardhalf':
            print('Half speed forward selected.')
            data = data_dd_forward_half
        elif arg.direction == 'rotatecw':
            print('Rotate Clockwise selected.')
            data = data_dd_rotate_cw
        elif arg.direction == 'rotateccw':
            print('Rotate Counterclockwise selected.')
            data = data_dd_rotate_ccw
        elif arg.direction == 'backward':
            print('Backward selected.')
            data = data_dd_backward_full
        elif arg.direction == 'backwardhalf':
            print('Half speed backward selected.')
            data = data_dd_backward_half
        else:
            print('Invalid Roomba direction.')
            return
    elif arg.drive == 'pwm':
        print('Drive PWM selected.')
        if arg.direction == 'forward':
            print('Forward selected.')
            data = data_pwm_forward_full
        elif arg.direction == 'forwardhalf':
            print('Half speed forward selected.')
            data = data_pwm_forward_half
        elif arg.direction == 'rotatecw':
            print('Rotate Clockwise selected.')
            data = data_pwm_rotate_cw
        elif arg.direction == 'rotateccw':
            print('Rotate Counterclockwise selected.')
            data = data_pwm_rotate_ccw
        elif arg.direction == 'backward':
            print('Backward selected.')
            data = data_pwm_backward_full
        elif arg.direction == 'backwardhalf':
            print('Half speed backward selected.')
            data = data_pwm_backward_half
        else:
            print('Invalid Roomba direction.')
            return
    
    if roomba != 'both':
        print('Starting Roomba OI...')
        if send(roomba, data_start):
            time.sleep(1)
            if arg.safemode == 'full':
                print('Warning: Setting Roomba to full control mode... Sensors are disabled in this mode.')
                send(roomba, data_full)
            elif arg.safemode == 'safe':
                print('Setting Roomba to safe mode.')
                send(roomba, data_safe)
            else:
                print('Error: Mode not recognized.')
                exit()
            time.sleep(1)
            print('Moving Roomba...')
            send(roomba, data)
            time.sleep(10)
            print('Stopping Roomba...')
            send(roomba, data_halt)
            time.sleep(1)
            print('Stopping Roomba OI...')
            send(roomba, data_stop)
        else:
            print('Failed to start Roomba OI at {}'.format(roomba))
    else:
        print('Starting Roomba0 OI...')
        if send('192.168.1.33', data_start):
            time.sleep(1)
            if arg.safemode == 'full':
                print('Warning: Setting Roomba0 to full control mode... Sensors are disabled in this mode.')
                send('192.168.1.33', data_full)
            elif arg.safemode == 'safe':
                print('Setting Roomba0 to safe mode.')
                send('192.168.1.33', data_safe)
            else:
                print('Error: Mode not recognized.')
                exit()
            time.sleep(1)
            print('Moving Roomba0...')
            send('192.168.1.33', data)
            time.sleep(10)
            print('Stopping Roomba0...')
            send('192.168.1.33', data_halt)
            time.sleep(1)
            print('Stopping Roomba0 OI...')
            send('192.168.1.33', data_stop)
        else:
            print('Failed to start Roomba0 OI.')
        print('Starting Roomba1 OI...')
        if send('192.168.1.38', data_start):
            time.sleep(1)
            if arg.safemode == 'full':
                print('Warning: Setting Roomba1 to full control mode... Sensors are disabled in this mode.')
                send('192.168.1.38', data_full)
            elif arg.safemode == 'safe':
                print('Setting Roomba1 to safe mode.')
                send('192.168.1.38', data_safe)
            else:
                print('Error: Mode not recognized.')
                exit()
            time.sleep(1)
            print('Moving Roomba1...')
            send('192.168.1.38', data)
            time.sleep(10)
            print('Stopping Roomba1...')
            send('192.168.1.38', data_halt)
            time.sleep(1)
            print('Stopping Roomba1 OI...')
            send('192.168.1.38', data_stop)
        else:
            print('Failed to start Roomba1 OI.')


if __name__ == '__main__':
    main()
