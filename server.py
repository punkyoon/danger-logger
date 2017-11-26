import os
import docker
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
_PASS_CODE = 'test'


def docker_start():
    global _SERVER_PATH
    subprocess.run(['sudo', 'docker-compose', '-f', _SERVER_PATH, 'up', '-d'])


def docker_down():
    global _SERVER_PATH
    subprocess.run(['sudo', 'docker-compose', '-f', _SERVER_PATH, 'down'])


def get_log():
    global _SERVER_PATH
    if is_docker_alive():
        output_result = subprocess.check_output([
            'sudo', 'docker-compose', '-f',
            _SERVER_PATH, 'logs', '--no-color'
        ])

        with open('logs.txt', 'wb') as f:
            f.write(output_result)

        return True
    else:
        return False


def is_docker_alive():
    _IS_ALIVE = False

    container_name_list = [
        'studyhard_nginx_1',
        'studyhard_worker_1',
        'studyhard_daphne_1',
        'studyhard_redis_1',
        'studyhard_postgres_1'
    ]

    docker_client = docker.from_env()
    container_list = docker_client.containers.list(
        filters={'status': 'running'}
    )

    if len(container_list) != 0:
        count = 0
        for container in container_list:
            if container.name in container_name_list:
                count += 1
        if count == len(container_name_list):
            _IS_ALIVE = True

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
                if not is_docker_alive():
                    msg = 'Web server on docker is started'
                    docker_start()
                else:
                    msg = 'Web server is already running on docker'

            elif data == 'stop':
                if is_docker_alive():
                    msg = 'We server on docker is stopped'
                    docker_down()
                else:
                    msg = 'Web server on docker is not running'

            elif data == 'status':
                msg = 'Web server on docker status: %s' % (is_docker_alive(),)

            elif data == 'log':
                if get_log():
                    with open('logs.txt', 'r') as f:
                        log_data = f.readlines()
                    for line in log_data:
                        msg += line
                    data_size = str(len(msg))
                    connection.send(data_size.encode())
                    connection.recv(1024).decode()
                else:
                    msg = 'Cannot get server log'

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
