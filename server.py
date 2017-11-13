import socket
import logging
import subprocess
import multiprocessing

from multiprocessing import Process


_SERVER_PATH = '/home/punk/study-hard'
_PASS_CODE = 'testestest'
_IS_ALIVE = False


def docker_start():
    subprocess.run(['docker-compose', 'up', '-d'])


def docker_down():
    subprocess.run(['docker-compose', 'down'])


def start_web_server():
    proc = Process(target=docker_start)
    _IS_ALIVE = True


def stop_web_server():
    proc = Process(target=docker_start)
    _IS_ALIVE = False


def is_alive_docker():
    return _IS_ALIVE


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
            # connection.sendall(data.encode())
            connection.send(data.encode())
            logger.debug('Sent data %r' % data)
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
