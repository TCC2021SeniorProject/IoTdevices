import paramiko
import sys

ssh0 = paramiko.SSHClient()
ssh1 = paramiko.SSHClient()

ssh0.load_system_host_keys()
ssh1.load_system_host_keys()

ssh0.connect('192.168.0.5', username='pi', password='ModelIoT')
ssh1.connect('192.168.0.6', username='pi', password='ModelIoT')

sftp0 = ssh0.open_sftp()
sftp1 = ssh1.open_sftp()

if len(sys.argv) > 1:
    localpath = sys.argv[1]
else:
    localpath = input('Enter the path for the local file: ')
remotepath = localpath

sftp0.put(localpath, remotepath)
sftp1.put(localpath, remotepath)

sftp0.close()
sftp1.close()

ssh0.close()
ssh1.close()

print('Done.')