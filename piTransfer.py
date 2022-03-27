import paramiko

ssh0 = paramiko.SSHClient()
ssh1 = paramiko.SSHClient()

ssh0.load_system_host_keys()
ssh1.load_system_host_keys()

ssh0.connect('192.168.0.7', username='pi', password='ModelIoT')
ssh1.connect('192.168.0.22', username='pi', password='ModelIoT')

sftp0 = ssh0.open_sftp()
sftp1 = ssh1.open_sftp()

localpath = input('Enter the path for the local file: ')
check = input('Would you like the file to have the same name? (Y/N) ')
if check == 'y' or 'Y':
    remotepath = localpath
else:
    remotepath = input('Enter the path for the new remote file: ')

sftp0.put(localpath, remotepath)
sftp1.put(localpath, remotepath)

sftp0.close()
sftp1.close()

ssh0.close()
ssh1.close()

print('Done.')