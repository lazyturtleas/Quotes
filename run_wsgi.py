from wsgiref.simple_server import make_server
from randomquotes.wsgi import application
import socket

if __name__ == "__main__":
    sock = socket.socket()
    sock.bind(('', 0))
    PORT = 8080
    sock.close()

    print(f"Starting WSGI server on http://127.0.0.1:{PORT}")

    with make_server('127.0.0.1', PORT, application) as httpd:
        httpd.serve_forever()