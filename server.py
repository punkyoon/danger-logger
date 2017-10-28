import os
import io
import socket

_IP = '0.0.0.0'
#_IP = '127.0.0.1'
_PORT = 8080

_BUFSIZ = 64
#_BUFSIZ = io.DEFAULT_BUFFER_SIZE

_PASSCODE = os.environ['PASSCODE']

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((_IP, _PORT))
server_socket.listen(1)

connection, addr = server_socket.accept()
print('[MSG] Client Connection - %s' % addr)

pass_code = connection.recv(_BUFSIZ)
if _PASSCODE != pass_code:
    print('[ERR] PASSCODE from client does not match')
    exit(1)

print('[MSG] Client authentication completed')

while True:
    cmd = connection.recv(_BUFSIZ)
    if cmd == 'quit':
        break

    print('[CMD] %s' % cmd)
    connection.send(cmd)    # Temporary code line

connection.close()
