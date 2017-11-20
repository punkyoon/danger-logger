import os
import socket
import hashlib
import logging
import subprocess
import multiprocessing

from multiprocessing import Process


_SERVER_PATH = os.path.join(
    '/home/punk/study-hard',
    'docker-compose.yaml'
)
_PASS_CODE = 'testtesttest'
_IS_ALIVE = False


def docker_start():
    subprocess.run(['docker-compose', '-f', _SERVER_PATH, 'up', '-d'])


def docker_down():
    subprocess.run(['docker-compose', '-f', _SERVER_PATH, 'down'])


def get_log():
    if is_docker_alive():
        output_result = subprocess.check_output([
            'docker-compose', '-f',
            _SERVER_PATH, 'logs', '--no-color'
        ])

        with open('logs.txt', 'wb') as f:
            f.write(output_result)

        return True
    else:
        return False


def start_web_server():
    global _IS_ALIVE
    _IS_ALIVE = True
    Process(target=docker_start)


def stop_web_server():
    global _IS_ALIVE
    _IS_ALIVE = True
    Process(target=docker_start)


def is_docker_alive():
    global _IS_ALIVE
    return _IS_ALIVE


def check_passcode(hash_value):
    global _PASS_CODE
    origin_value = hashlib.sha256(_PASS_CODE.encode()).hexdigest()
    if origin_value == hash_value:
        return True
    else:
        return False


def handle(connection, addr):
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger('process-%r' % (addr,))

    pass_code = connection.recv(1024).decode()
    if not check_passcode(pass_code):
        connection.send('False'.encode())
        logger.debug('Invalid passcode - connection refused')
        connection.close()
        exit(0)

    msg = 'Valid passcode - connected successfully'
    connection.send(msg.encode())
    logger.debug(msg)

    try:
        logger.debug('Connected %r at %r' % (connection, addr))
        while True:
            data = connection.recv(1024).decode()
            if data == '':
                logger.debug('socket closed remotely')
                break
            logger.debug('Received data %r' % data)

            msg = ''
            if data == 'start':
                if is_docker_alive():
                    msg = 'Web server on docker is started'
                    start_web_server()
                else:
                    msg = 'Web server is already running on docker'

            elif data == 'stop':
                if is_docker_alive():
                    msg = 'We server on docker is stopped'
                    stop_web_server()
                else:
                    msg = 'Web server on docker is not running'

            elif data == 'status':
                msg = 'Web server on docker status: %s' % (is_docker_alive(),)

            elif data == 'quit':
                msg = 'quit'

            else:
                msg = 'Invalid command'

            # connection.sendall(data.encode())
            logger.debug(msg)
            connection.send(msg.encode())
            logger.debug('Sent data %r' % msg)
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
