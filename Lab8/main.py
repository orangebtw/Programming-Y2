from http import HTTPStatus
from http.server import HTTPServer, BaseHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
from urllib.parse import parse_qsl
from pathlib import Path

from controllers.userController import UserController
from controllers.currenciesController import CurrenciesController
from controllers.authorController import AuthorController
from controllers.databaseController import CurrencyDatabase, UserDatabase, UserCurrencyDatabase

from utils.response import *

MIME_TYPES: dict = {
    '.css': 'text/css',
    '.html': 'text/html',
    '.js': 'text/javascript'
}

env = Environment(
    loader=FileSystemLoader('./templates/'),
    autoescape=select_autoescape()
)

template_404 = env.get_template("404.html")
template_403 = env.get_template("403.html")

currency_database = CurrencyDatabase()
user_database = UserDatabase()
user_currencies_database = UserCurrencyDatabase()

class HttpHandler(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        self.user_controller = UserController(user_database, user_currencies_database, currency_database, env)
        self.author_controller = AuthorController(env)
        self.currencies_controller = CurrenciesController(currency_database, env)
        
        super().__init__(request, client_address, server)
    
    def do_GET(self):
        path = self.path
        if len(path) > 1:
            path = path.removesuffix('/')

        params = {}

        i = self.path.find('?')
        if i >= 0:
            path = self.path[:i]
            params = dict(parse_qsl(self.path[(i + 1):]))
            
        if path.startswith('/static'):
            self.serve_static(path.removeprefix('/static'))
            return
            
        response = self.author_controller.handle_get(path, params)
        if response is not None:
            handle_response(self, response)
            return
        
        response = self.user_controller.handle_get(path, params)
        if response is not None:
            handle_response(self, response)
            return
        
        response = self.currencies_controller.handle_get(path, params)
        if response is not None:
            handle_response(self, response)
            return
        
        self.page404()

    def do_POST(self):
        self.send_response(HTTPStatus.BAD_REQUEST)
        self.end_headers()

    def page404(self):
        respond_html(self, template_404.render(), status=404)

    def page403(self):
        respond_html(self, template_403.render(), status=403)

    def serve_static(self, path: str):
        p = Path(path)
        mime_type = MIME_TYPES.get(p.suffix, "application/octet-stream")
        try:
            with open('./static' + path, 'rb') as f:
                respond_bytes(self, f.read(), mime_type)
        except IsADirectoryError:
            self.page403()
        except FileNotFoundError:
            self.page404()

def run_server(address: str, port: int):
    HTTPServer((address, port), HttpHandler).serve_forever()

def main():
    run_server('', 1234)

if __name__ == "__main__":
    main()
