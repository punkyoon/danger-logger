import os
import io
import socket

_IP = '0.0.0.0'
#_IP = '127.0.0.1'
_PORT = 8080

_BUFSIZ = 64
#_BUFSIZ = io.DEFAULT_BUFFER_SIZE

#_PASSCODE = os.environ['PASSCODE']
_PASSCODE = 'test'

print('[MSG] Creating server socket ...')
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((_IP, _PORT))
server_socket.listen(1)
print('[MSG] Server socket is created')

connection, addr = server_socket.accept()
print('[MSG] Client Connection - %s' % str(addr[0]))

pass_code = connection.recv(_BUFSIZ).decode()
if _PASSCODE != pass_code:
    print('[ERR] PASSCODE from client does not match')
    connection.send('False'.encode())
    exit(1)

connection.send('True'.encode())
print('[MSG] Client authentication completed')

while True:
    cmd = connection.recv(_BUFSIZ).decode()

    print('[CMD] %s' % cmd)
    connection.send(cmd.encode())    # Temporary code line

    if cmd == 'quit':
        connection.close()
        break

print('[MSG] Closing server socket ...')
server_socket.shutdown(1)
server_socket.close()
