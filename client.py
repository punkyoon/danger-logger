import socket


if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('localhost', 8080))
    while True:
        cmd = input('[INP] command: ')
        #sock.sendall(cmd.encode())
        sock.send(cmd.encode())

        result = sock.recv(1024).decode()
        print(result)
        if result == 'quit':
            break

    sock.close()
