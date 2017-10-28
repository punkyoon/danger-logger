import io
import socket

_SERVER_IP = '127.0.0.1'
_PORT = 8080

#_BUFSIZ = io.DEFAULT_BUFFER_SIZE
_BUFSIZ = 64

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((_SERVER_IP, _PORT))

_passcode = input('[INP] PASSCODE: ')

client_socket.send(_passcode.encode())
is_passed = client_socket.recv(_BUFSIZ).decode()

if is_passed != 'True':
    print('[MSG] PASSCODE does not match')
    exit(1)

while True:
    cmd = input('[INP] command: ')
    client_socket.send(cmd.encode())
    
    response_data = client_socket.recv(_BUFSIZ).decode()
    if response_data == 'quit':
        break
    print('[MSG] %s' % response_data)    # Temporary code line

print('[MSG] Closing client socket ...')
client_socket.close()
