# Simple paramiko script to set values on a list of nodes

import paramiko, time,sys

def check_args():
        if len(sys.argv) == 4:
             loadup()
        else:
             print('Not enough arguments')
             sys.exit


def loadup():
    try:
        with open(sys.argv[1], 'r') as my_file:
            for line in my_file:
                connect_me(line)
    except Exception as error:
         print(f'./test filename username password \n {error}')

def connect_me(line):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print(f'Connecting to: { line }')
    ssh.connect(line.strip('\n'), username=sys.argv[2], password=sys.argv[3],look_for_keys=False,allow_agent=False)
    print('Successfully connected to %s' % line)

    remote_conn = ssh.invoke_shell()
    output = remote_conn.recv(1000)

    # Disable paging on Brocade.
    remote_conn.send('pwd\n')
    time.sleep(2)
    # Clearing output.
    if remote_conn.recv_ready():
        output = remote_conn.recv(1000)

    # Check interface status.
    remote_conn.send('ls -l /\n') # I only want output from this command.
    time.sleep(2)
    # Getting output I want.
    if remote_conn.recv_ready():
        output = remote_conn.recv(5000)

    # Display output
    for line in output.decode('utf-8').splitlines():
            print(line)

check_args()