import socket
import hashlib
import getpass


# Main cod
if __name__ == '__main__':
    _IS_PASSED = False

    # Creating socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('localhost', 8080))    # Server IP and port

    # Authenticate user
    cmd = getpass.getpass('[AUTH] passcode: ')
    pass_hash = hashlib.sha256(cmd.encode()).hexdigest()
    sock.send(pass_hash.encode())

    # Check passcode
    is_passed = sock.recv(1024).decode()
    if is_passed == 'False':
        print('[MSG]Invalid passcode')
        sock.close()
        exit(0)

    print('[MSG]Valid passcode')
    while True:
        # Service list menu
        print('=================MANAGER=================')
        print('1. start: server start')
        print('2. stop: server stop')
        print('3. status: check server status')
        print('4. log: get server log file')
        print('5. quit: quit program')
        print('=========================================')
        cmd = input('command > ')
        print()

        if cmd == 'start' or cmd == 'stop':
            print('[MSG]Loading..')

        # Sending command
        sock.send(cmd.encode())

        result = sock.recv(1024).decode()

        if cmd == 'log' and result != 'Cannot get server log':
            ok_msg = 'ready'
            sock.send(ok_msg.encode())
            data_size = int(result)
            result = sock.recv(data_size).decode()
            with open('logs.txt', 'w') as f:
                f.write(result)
            print('[MSG]Saved logs.txt')
        else:
            print(result)
        print()

        # Shutdown service
        if result == 'quit':
            print('[MSG]Shutdown..')
            break

    sock.close()
