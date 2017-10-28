import io
import socket

_SERVER_IP = '127.0.0.1'
_PORT = 8080

_BUFSIZ = io.DEFAULT_BUFFER_SIZE

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((_SERVER_IP, _PORT))

while True:
    cmd = input()
    client_socket.send(cmd)
    
    response_data = client_socket.recv(_BUFSIZ)
    if response_data == 'quit':
        break
    print('[MSG] %s' % response_data)    # Temporary code line

client_socket.close()
