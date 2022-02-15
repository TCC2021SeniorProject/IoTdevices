import paramiko

ssh0 = paramiko.SSHClient()
ssh1 = paramiko.SSHClient()

ssh0.connect('192.168.1.4', username='pi', password='ModelIoT')
ssh1.connect('192.168.1.36', username='pi', password='ModelIoT')

sftp0 = ssh.open_sftp()
sftp1 = ssh.open_sftp()

localpath = input('Enter the path for the local file:')
remotepath = input('Enter the path for the new remote file:')

sftp0.put(localpath, remotepath)
sftp1.put(localpath, remotepath)

sftp0.close()
sftp1.close()

ssh0.close()
ssh1.close()