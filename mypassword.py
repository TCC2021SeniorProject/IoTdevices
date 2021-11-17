from pprint import pformat
import json
import socket
import ssl
import sys
import time
from ast import literal_eval
import configparser


def receive_udp():
    #set up UDP socket to receive data from robot
    port = 5678
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(10)
    s.bind(("", port))  #bind all interfaces to port
    print("waiting on port: {} for data".format(port))
    message = 'irobotmcs'
    s.sendto(message.encode(), ('192.168.1.33', port))
    roomba_dict = {}
    while True:
        try:
            udp_data, addr = s.recvfrom(1024)   #wait for udp data)
            if udp_data and udp_data.decode() != message:
                try:
                    parsedMsg = json.loads(udp_data.decode())
                    if addr[0] not in roomba_dict.keys():
                        s.sendto(message.encode(), (addr, port))
                        roomba_dict[addr[0]]=parsedMsg
                        print('Robot at IP: {} Data: {}'.format(addr[0], json.dumps(parsedMsg, indent=2)))
                except Exception as e:
                    print("json decode error: {}".format(e))
                    print('RECEIVED: {}'.format(pformat(udp_data)))

        except socket.timeout:
            break
    s.close()
    return


def go(addr):
    # Send MQTT magic packet to addr
    # This is 0xf0 (mqtt reserved) 0x05(data length) 0x91???????? (data)
    # Should tell Roomba to move forward at full speed.
    # Uses 10 second timeout for socket connection
    packet1 = bytes.fromhex('f00180')
    #packet2 = bytes.fromhex('f00289FFFF') # spin cw
    #packet2 = bytes.fromhex('f00087') # clean
    packet2 = bytes.fromhex('f005efcc3b2900') # retrieve password
    packet3 = bytes.fromhex('f001ad')
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(10)

    #context = ssl.SSLContext(ssl.PROTOCOL_TLS)
    context = ssl.SSLContext()
    context.set_ciphers('DEFAULT@SECLEVEL=2:HIGH:!DH:!aNULL')
    #context.set_ciphers('DEFAULT@SECLEVEL=2:HIGH:!aNULL:!MD5:!RC4')
    #context.set_ciphers('DEFAULT@SECLEVEL=2:HIGH:!aNULL:!kRSA:!MD5:!RC4')
    wrappedSocket = context.wrap_socket(sock)

    no_error = True
    try:
        wrappedSocket.connect((addr, 8883))
        print('Connection successful.')
        print('Sending packet.')
        wrappedSocket.send(packet2)
        data = b''
        print('Waiting for data...')
        while len(data) < 37:
            data_received = wrappedSocket.recv(1024)
            data += data_received
            if len(data_received) == 0:
                print('>>> SOCKET CLOSED, DATA LENGTH: {}'.format(len(data)))
                break
        password = str(data[7:].decode().rstrip('\x00')) #for i7 - has null termination
        print('Password: \'{}\''.format(password))
        print(data)
        print('Packet sent.')
        wrappedSocket.close()
        print('Connection closed.')
        return data
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
        '-O','--oneroomba',
        action='store',
        type=str,
        default='2',
        help='Choose a Roomba. \'0\' (Roomba0), \'1\' (Roomba1), or \'2\' (Both).')
    parser.add_argument(
        '-D','--direction',
        action='store',
        type=str,
        default='forward',
        help='Choose a direction. \'forward\', \'forwardhalf\'(INOP), \'rotatecw\', \'rotateccw\', \'spinonleft\', \'spinonright\', \'backward\'(INOP), \'backwardhalf\'(INOP)')
    arg = parser.parse_args()

    #-------- Movement Data ----------------
    data_start = 'f00180'                   # Data to start OI
    data_forward_full = 'f002898000'        # Data for full speed forward motion
    data_forward_half = 'f002894000'        # Data for half speed forward motion
    data_rotate_cw = 'f00289FFFF'           # Data to spin clockwise
    data_rotate_ccw = 'f002890001'          # Data to spin counter-clockwise
    data_backward_full = 'f002897FFF'       # Data for full speed backward motion
    #data_backward_half = 'f00289????'      # Data for half speed backward motion
    data_stop = 'f001ad'                    # Data to stop OI
    
    receive_udp()
    go('192.168.1.33')
    #go('192.168.1.38')


if __name__ == '__main__':
    main()
