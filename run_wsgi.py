from wsgiref.simple_server import make_server
from randomquotes.wsgi import application
import socket

if __name__ == "__main__":
    PORT = 8080
    print(f"Starting WSGI server on http://127.0.0.1:{PORT}")
    with make_server('127.0.0.1', PORT, application) as httpd:
        httpd.serve_forever()