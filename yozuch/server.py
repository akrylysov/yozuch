"""
Preview server.
"""
import http.server
import os
import socketserver
import traceback
from threading import Thread
from yozuch import logger
from yozuch.watcher import watch
from yozuch.notification_server import WebSocketNotificationServer


class HTTPServer(socketserver.ThreadingTCPServer):
    allow_reuse_address = True


def serve(directory, build_command, ports):

    output_dir = '_yozuch_cache_'
    os.chdir(build_command(output_dir))

    autoreload_server = WebSocketNotificationServer()

    def cmd():
        try:
            build_command(output_dir)
            autoreload_server.broadcast_message('reload')
        except:
            traceback.print_exc()

    stop_watcher = watch(directory, cmd)

    http_server_port, autoreload_server_port = ports

    handler = http.server.SimpleHTTPRequestHandler
    httpd = HTTPServer(('', http_server_port), handler)

    autoreload_server_thread = Thread(target=autoreload_server.start, args=(autoreload_server_port,))
    autoreload_server_thread.start()

    logger.info('Serving content on http://127.0.0.1:{}/'.format(http_server_port))
    logger.info('Auto reload server on port {}'.format(autoreload_server_port))
    logger.info('Press "Ctrl+C" to exit')

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        stop_watcher()
        logger.info('Shutting down server...')
        autoreload_server.stop()
        httpd.socket.close()
        autoreload_server_thread.join()
