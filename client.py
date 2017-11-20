import socket
import hashlib


if __name__ == '__main__':
    _IS_PASSED = False

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('localhost', 8080))

    cmd = input('[AUTH] passcode: ')
    pass_hash = hashlib.sha256(cmd.encode()).hexdigest()
    sock.send(pass_hash.encode())

    is_passed = sock.recv(1024).decode()
    if is_passed == 'False':
        print('[MSG]Invalid passcode')
        sock.close()
        exit(0)

    print('[MSG]Valid passcode')
    while True:
        cmd = input('[INP] command: ')
        #sock.sendall(cmd.encode())
        sock.send(cmd.encode())

        result = sock.recv(1024).decode()
        print(result)
        if result == 'quit':
            print('[MSG]Shutdown..')
            break

    sock.close()
