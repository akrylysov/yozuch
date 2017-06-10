"""
WebSocket server which is only able to send broadcast notification messages to all connected clients.
"""

import socket
import hashlib
import base64
import threading


def _parse_headers(data):
    headers = {}
    for line in data.splitlines():
        parts = line.split(': ', 2)
        if len(parts) == 2:
            headers[parts[0].lower()] = parts[1]
    return headers


class WebSocketNotificationServer(object):

    HANDSHAKE_RESPONSE = 'HTTP/1.1 101 Switching Protocols\r\n' + \
        'Upgrade: websocket\r\n' + \
        'Connection: Upgrade\r\n' + \
        'Sec-WebSocket-Accept: {}\r\n' + \
        '\r\n'

    def __init__(self):
        self._lock = threading.Lock()
        self._clients = []
        self._running = False
        self._socket = None

    def _handshake(self, client):
        data = client.recv(2048)
        if not data:
            return False
        headers = _parse_headers(data.decode())
        key = headers.get('sec-websocket-key', '')
        accept = base64.b64encode(hashlib.sha1((key + '258EAFA5-E914-47DA-95CA-C5AB0DC85B11').encode()).digest())
        response = self.HANDSHAKE_RESPONSE.format(accept.decode())
        client.send(response.encode())
        return True

    def _handle_client(self, client):
        client.settimeout(None)
        if self._handshake(client):
            client.settimeout(2)
            with self._lock:
                self._clients.append(client)
            while self._running:
                try:
                    data = client.recv(2048)
                    if not data:
                        break
                except socket.timeout:
                    pass
                except Exception:
                    break
        with self._lock:
            try:
                self._clients.remove(client)
            except ValueError:
                pass
        client.close()

    def broadcast_message(self, data):
        response = bytearray([0b10000001, len(data)])
        response.extend(data.encode())
        with self._lock:
            for client in list(self._clients):  # make a copy of self._clients
                try:
                    client.send(response)
                except Exception:
                    try:
                        self._clients.remove(client)
                    except ValueError:
                        pass

    def start(self, port):
        self._running = True
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._socket.bind(('', port))
        self._socket.listen(5)
        self._socket.settimeout(2)
        while self._running:
            try:
                client, _ = self._socket.accept()
                if self._running:
                    threading.Thread(target=self._handle_client, args=(client,)).start()
            except socket.timeout:
                pass

    def stop(self):
        self._running = False
        self._socket.close()
        with self._lock:
            for client in self._clients:
                client.close()
