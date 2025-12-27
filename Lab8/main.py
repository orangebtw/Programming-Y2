from http import HTTPStatus
from http.server import HTTPServer, BaseHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
from urllib.parse import parse_qsl
from pathlib import Path
from utils.currencies_api import get_currencies

from models.app import App
from models.author import Author
from models.user import User
from models.user_currency import UserCurrency

from controllers.userController import UserController
from controllers.currenciesController import CurrenciesController
from controllers.authorController import AuthorController
from controllers.databaseController import CurrencyDatabase, UserDatabase, UserCurrencyDatabase

from utils.response import *

USERS = (
    User(1, 'Илон Маск'),
    User(2, 'Дональд Трамп'),
    User(3, 'Барак Обама'),
)

USER_CURRENCIES = (
    UserCurrency(1, 1, 'R01235'),
    UserCurrency(2, 1, 'R01375'),
    UserCurrency(3, 1, 'R01035'),
    
    UserCurrency(4, 2, 'R01235'),
    UserCurrency(5, 2, 'R01375'),
    UserCurrency(6, 2, 'R01035'),
    
    UserCurrency(7, 3, 'R01235'),
)

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
        self.user_controller = UserController(self, user_database, user_currencies_database, currency_database, env)
        self.author_controller = AuthorController(self, env)
        self.currencies_controller = CurrenciesController(self, currency_database, env)
        
        super().__init__(request, client_address, server),
    
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
            
        if self.author_controller.handle_get(path, params):
            return
        
        if self.user_controller.handle_get(path, params):
            return
        
        if self.currencies_controller.handle_get(path, params):
            return
        
        self.page404()

    def do_POST(self):
        self.send_response(HTTPStatus.BAD_REQUEST)

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
