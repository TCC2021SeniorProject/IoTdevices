from pprint import pformat
import socket
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
#        print('Connection successful.')
        wrappedSocket.send(packet)
        print(f'\'{data}\' sent to {addr} as {packet}')
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
    #-------- Movement Data ----------------
    # Basics
    data = ''
    data_mqtt = 'f0'
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
    
    data = data_start + data_safe + data_clean
    send('192.168.1.33', data)
    send('192.168.1.38', data)


if __name__ == '__main__':
    main()
