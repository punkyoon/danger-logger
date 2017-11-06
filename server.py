import os
import io
import socket
import logging
import multiprocessing

def handle(connection, addr):
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger('process-%r' % (addr,))
    try:
        logger.debug('Connected %r at %r' % (connection, addr))
        while True:
            data = connection.recv(1024).decode()
            if data == '':
                logger.debug('socket closed remotely')
                break
            logger.debug('Received data %r' % data)
            #connection.sendall(data.encode())
            connection.send(data.encode())
            logger.debug('Sent data')
    except:
        logger.exception('Problem handling request')
    finally:
        logger.debug('Closing socket')
        connection.close()


class Server(object):
    def __init__(self, hostname, port):
        self.logger = logging.getLogger('server')
        self.hostname = hostname
        self.port = port

    def start(self):
        self.logger.debug('listening')
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.hostname, self.port))
        self.socket.listen(1)

        while True:
            conn, addr = self.socket.accept()
            self.logger.debug('Got connection')
            process = multiprocessing.Process(target=handle, args=(conn, addr))
            process.daemon = True
            process.start()

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    server = Server('0.0.0.0', 8080)
    try:
        logging.info('Listening')
        server.start()
    except:
        logging.exception('Unexpected exception')
    finally:
        logging.info('Shutting down')
        for process in multiprocessing.active_children():
            logging.info('Shutting down process %r' % process)
            process.terminate()
            process.join()
    logging.info('all done')

'''
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
'''
