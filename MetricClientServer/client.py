import socket
import time


class ClientError(Exception):
    pass


class Client:
    def __init__(self, host, port, timeout=None):
        try:
            self._conn = socket.create_connection((host, port))
            self._conn.settimeout(timeout)
        except socket.error:
            raise ClientError

    def get(self, metric_name):
        self._conn.sendall(f'get {metric_name}\n'.encode('utf8'))
        resp = self._conn.recv(1024).decode('utf8')
        if resp == 'ok\n\n':
            return {}
        elif resp == 'error\nwrong command\n\n' or resp[:3] != 'ok\n':
            raise ClientError('Wrong command')
        else:
            try:
                d = {}
                resp = resp.rstrip('\n\n').lstrip('ok\n').split('\n')
                resp = [it.split(' ') for it in resp]
                for key, value, timestamp in resp:
                    if key not in d.keys():
                        d[key] = [(int(timestamp), float(value))]
                    else:
                        d[key].append((int(timestamp), float(value)))

                for key in d.keys():
                    d[key].sort(key=lambda i: i[0])
                return d

            except Exception:
                raise ClientError('Incorrect data')

    def put(self, metric_name, value, timestamp=None):
        if not timestamp:
            timestamp = int(time.time())
        self._conn.sendall(f'put {metric_name} {value} {timestamp}\n'.encode('utf8'))
        resp = self._conn.recv(1024).decode('utf8')
        if resp == 'ok\n\n':
            return
        else:
            raise ClientError

    def close(self):
        try:
            self._conn.close()
            print('Client socket closed')
        except socket.error:
            raise ClientError('Cannot close connection')
