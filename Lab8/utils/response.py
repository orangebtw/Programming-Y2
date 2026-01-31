from http import HTTPStatus
from http.server import BaseHTTPRequestHandler

from common import Response

def respond_bytes(handler: BaseHTTPRequestHandler, b: bytes, mime_type: str, status: HTTPStatus = HTTPStatus.OK):
    handler.send_response(status)
    handler.send_header('Content-Type', mime_type)
    handler.send_header('Content-Length', len(b))
    handler.end_headers()
    handler.wfile.write(b)

def respond_html(handler: BaseHTTPRequestHandler, html: str, status: HTTPStatus = HTTPStatus.OK):
    respond_bytes(handler, html.encode('utf-8'), 'text/html', status=status)
    
def redirect(handler: BaseHTTPRequestHandler, url: str):
    handler.send_response(301)
    handler.send_header('Location', url)
    handler.end_headers()
    
def handle_response(handler: BaseHTTPRequestHandler, response: Response):
    handler.send_response(response.status)
    for name, value in response.headers.items():
        handler.send_header(name, value)
    handler.end_headers()
    if response.content is not None:
        handler.wfile.write(response.content)
        