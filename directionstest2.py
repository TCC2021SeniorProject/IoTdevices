from pprint import pformat
import socket
import serial
import ssl
import sys
import time
from ast import literal_eval

def send(addr, data):
    packet = data.encode()
    serialRoomba = serial.Serial('192.168.1.33') # ttyUSBx format on Linux
    serialRoomba.baudrate = 115200 # set Baud rate to Roomba default
    serialRoomba.bytesize = 24     # Number of data bytes = 3
    serialRoomba.parity   = 'N'    # No parity
    serialRoomba.stopbits = 1      # Number of Stop bits = 1
    time.sleep(3)
    serialRoomba.write(packet)     # Transmit packet over serial
    serialRoomba.close()           # Close the port


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
