from pprint import pformat
import socket
import serial
import ssl
import sys
import time
from ast import literal_eval

def send(addr, data):
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
        ser = serial.Serial(8883, 115200)
        ser.write(packet)
        #wrappedSocket.send(packet)
        print(f'\'{data}\' sent to {addr} as {packet}')
        wrappedSocket.close()
        return no_error
    except socket.timeout as e:
        no_error = False
        print('Connection Timeout Error (for {}): {}'.format(addr, e))
    except (ConnectionRefusedError, OSError) as e:
        no_error = False
        if e.errno == 111:      #errno.ECONNREFUSED
            print('Unable to Connect to roomba at ip {}. Make sure nothing else is connected (app?), '
                            'as only one connection at a time is allowed'.format(addr))
        elif e.errno == 113:    #errno.No Route to Host
            print('Unable to contact roomba on ip {}. Is the ip correct?'.format(addr))
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
        '-m','--direction',
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
        '-d','--drive',
        action='store',
        type=str,
        default='clean',
        help='Choose a drive mode. \'drive\', \'dd\', \'pwm\', \'clean\', or \'dock\'.')
    arg = parser.parse_args()

    #-------- Movement Data ----------------
    # Basics
    data = 'f0'
    data_start = '80'                   # Data to start OI
    data_safe = '83'                    # Data for safe mode
    data_full = '84'                    # Data for full mode
    data_clean = '87'                   # Data for clean
    data_dock = '8f'                    # Data for dock
    data_halt = '9100000000'            # Data to stop Roomba movement
    data_stop = 'ad'                    # Data to stop OI
    # Drive
    data_forward_full = '898000'        # Data for full speed forward motion
    data_forward_half = '8900fa0000'    # Data for half speed forward motion
    data_rotate_cw = '89ffff'           # Data to spin clockwise
    data_rotate_ccw = '890001'          # Data to spin counter-clockwise
    data_backward_full = '897fff'       # Data for full speed backward motion
    data_backward_half = '89ff060000'   # Data for half speed backward motion
    # Drive Direct
    data_dd_forward_full = '9101f401f4'
    data_dd_forward_half = '9100ff00ff'
    data_dd_rotate_cw = '91fe0c01f4'
    data_dd_rotate_ccw = '9101f4fe0c'
    data_dd_backward_full = '91fe0cfe0c'
    data_dd_backward_half = '91ff01ff01'
    # Drive PWM
    data_pwm_forward_full = '9200ff00ff'
    data_pwm_forward_half = '9200880088'
    data_pwm_rotate_cw = '92ff0100ff'
    data_pwm_rotate_ccw = '9200ffff01'
    data_pwm_backward_full = '92ff01ff01'
    data_pwm_backward_half = '9288018801'
    
    if arg.oneroomba == '0':
        roomba = '192.168.1.33'
    elif arg.oneroomba == '1':
        roomba = '192.168.1.38'
    elif arg.oneroomba == '2':
        roomba = 'both'
    else:
        print('Invalid Roomba selection.')
        
    data += data_start
    
    if arg.safemode == 'full':
        print('Warning: Setting Roomba(s) to full control mode... Sensors are disabled in this mode.')
        data += data_full
    elif arg.safemode == 'safe':
        print('Setting Roomba(s) to safe mode.')
        data += data_safe
    else:
        print('Error: Mode not recognized.')
        exit()
    
    if arg.drive == 'clean':
        print('Clean selected.')
        data += data_clean
    elif arg.drive == 'dock':
        print('Dock selected.')
        data += data_dock
    elif arg.drive == 'drive':
        print('Drive selected.')
        if arg.direction == 'forward':
            print('Forward selected.')
            data += data_forward_full
        elif arg.direction == 'forwardhalf':
            print('Half speed forward selected.')
            data += data_forward_half
        elif arg.direction == 'rotatecw':
            print('Rotate Clockwise selected.')
            data += data_rotate_cw
        elif arg.direction == 'rotateccw':
            print('Rotate Counterclockwise selected.')
            data += data_rotate_ccw
        elif arg.direction == 'backward':
            print('Backward selected.')
            data += data_backward_full
        elif arg.direction == 'backwardhalf':
            print('Half speed backward selected.')
            data += data_backward_half
        else:
            print('Invalid Roomba direction.')
            return
    elif arg.drive == 'dd':
        print('Drive Direct selected.')
        if arg.direction == 'forward':
            print('Forward selected.')
            data += data_dd_forward_full
        elif arg.direction == 'forwardhalf':
            print('Half speed forward selected.')
            data += data_dd_forward_half
        elif arg.direction == 'rotatecw':
            print('Rotate Clockwise selected.')
            data += data_dd_rotate_cw
        elif arg.direction == 'rotateccw':
            print('Rotate Counterclockwise selected.')
            data += data_dd_rotate_ccw
        elif arg.direction == 'backward':
            print('Backward selected.')
            data += data_dd_backward_full
        elif arg.direction == 'backwardhalf':
            print('Half speed backward selected.')
            data += data_dd_backward_half
        else:
            print('Invalid Roomba direction.')
            return
    elif arg.drive == 'pwm':
        print('Drive PWM selected.')
        if arg.direction == 'forward':
            print('Forward selected.')
            data += data_pwm_forward_full
        elif arg.direction == 'forwardhalf':
            print('Half speed forward selected.')
            data += data_pwm_forward_half
        elif arg.direction == 'rotatecw':
            print('Rotate Clockwise selected.')
            data += data_pwm_rotate_cw
        elif arg.direction == 'rotateccw':
            print('Rotate Counterclockwise selected.')
            data += data_pwm_rotate_ccw
        elif arg.direction == 'backward':
            print('Backward selected.')
            data += data_pwm_backward_full
        elif arg.direction == 'backwardhalf':
            print('Half speed backward selected.')
            data += data_pwm_backward_half
        else:
            print('Invalid Roomba direction.')
            return
    
    data += data_stop
    
    data_size = str(int(len(data[2:])/2))
    if len(data_size) == 1:
        data_size = '0' + data_size
    data = data[:2] + data_size + data[2:]
    
    if roomba != 'both':
        if not send(roomba, data):
            print('Failed to connect to Roomba at {}'.format(roomba))
            exit()
    else:
        if not send('192.168.1.33', data):
            print('Failed to connect to Roomba0.')
        if not send('192.168.1.38', data):
            print('Failed to connect to Roomba1.')


if __name__ == '__main__':
    main()
