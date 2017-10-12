import logging
import socket


LOGGER = logging.getLogger(__name__)


class DataStreamClient:
    HOST = '127.0.0.1'
    PORT = 3092

    def __init__(self, processor):
        self._sock = None
        self._sock_file = None

        self._processor = processor

        self._should_stop = False

    def start(self):
        LOGGER.info('Starting up...')
        LOGGER.info('Connecting to %s:%d...',
            DataStreamClient.HOST,
            DataStreamClient.PORT
        )

        self._sock = socket.create_connection(
            (DataStreamClient.HOST, DataStreamClient.PORT)
        )

        LOGGER.info('Connected!')

        self._sock_file = self._sock.makefile()
        while not self._should_stop:
            self._loop()

        LOGGER.info('Shutting down...')

    def stop(self):
        self._should_stop = True

    def _loop(self):
        data = self._sock_file.readline().strip()
        data_split = data.split(' ')

        self._processor.queue_data({
            'timestamp': float(data_split[0]),
            'rssi': [int(d) for d in data_split[1:]]
        })
