import paramiko
import netifaces as ni


def fileTransfer(localpath, remotepath):

    ssh = paramiko.SSHClient()
    ssh.load_system_host_keys()

    local_ip = ni.ifaddresses('wlan0')[ni.AF_INET][0]['addr']
    if local_ip == '192.168.0.7':
        ip = '192.168.0.7'
    else:
        ip = '192.168.0.22'

    ssh.connect(ip, username='pi', password='ModelIoT')
    sftp = ssh.open_sftp()

    sftp.put(localpath, remotepath)

    sftp.close()
    ssh.close()