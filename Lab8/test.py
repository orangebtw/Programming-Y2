import unittest
from unittest.mock import MagicMock

from io import BytesIO
from jinja2 import Environment, FileSystemLoader, select_autoescape

from http import HTTPStatus

from utils.currencies_api import get_currencies
from models.currency import Currency
from models.user import User
from models.user_currency import UserCurrency
from main import HttpHandler

from common import APP, PAGES, Response

from controllers.currenciesController import CurrenciesController
from controllers.authorController import AuthorController
from controllers.userController import UserController

class MockRequest:
    def __init__(self, request: str):
        self.request = request.encode('utf-8')
    
    def makefile(self, *args, **kwargs):
        return BytesIO(self.request)
    
    def sendall(self, *args, **kwargs):
        pass

class TestHttpHandler(HttpHandler):
    wbufsize = 1
    
    def finish(self):
        self.wfile.flush()
        self.rfile.close()
        
    def version_string(self):
        return "TestServer"
    
    def date_time_string(self, timestamp = None):
        return "123"

class Test(unittest.TestCase):
    def setUp(self):
        self.maxDiff = 9999
        
        env = Environment(
            loader=FileSystemLoader('./templates/'),
            autoescape=select_autoescape()
        )

        self.template_index = env.get_template("index.html")
        self.template_users = env.get_template("users.html")
        self.template_user = env.get_template("user.html")
        self.template_author = env.get_template("author.html")
        self.template_currencies = env.get_template("currencies.html")
        self.template_404 = env.get_template("404.html")
        
        self.mock_currencies_db = MagicMock()
        self.mock_currencies_db.get_all.return_value = [Currency('1', 'USD', 'Доллар', 75, 1), Currency('2', 'EUR', 'Евро', 90, 1)]
        self.mock_currencies_db.get_by_id.return_value = Currency('1', 'USD', 'Доллар', 75, 1)
        self.mock_currencies_db.update_by_char_code.return_value = None
        self.mock_currencies_db.delete.return_value = None
        
        self.mock_users_db = MagicMock()
        self.mock_users_db.get_all.return_value = [User(1, "Вася"), User(2, "Петя"), User(3, 'Дима')]
        self.mock_users_db.get_by_id.return_value = User(1, "Вася")
        self.mock_users_db.delete.return_value = None
        
        self.mock_user_currencies_db = MagicMock()
        self.mock_user_currencies_db.get_all.return_value = [UserCurrency(1, "1", 1), UserCurrency(2, "1", 2), UserCurrency(3, "2", 3)]
        self.mock_user_currencies_db.get_by_user_id.return_value = [UserCurrency(1, "1", 1)]
        self.mock_user_currencies_db.delete.return_value = None
        
        self.author_controller = AuthorController(env=env)
        self.user_controller = UserController(users_db=self.mock_users_db, currencies_db=self.mock_currencies_db, user_currencies_db=self.mock_user_currencies_db, env=env)
        self.currencies_controller = CurrenciesController(db=self.mock_currencies_db, env=env)
    
    def test_get_currencies(self):
        currencies = get_currencies(['R01235', 'R01375'])
        self.assertEqual(len(currencies), 2)
        
        for currency in currencies:
            self.assertIsInstance(currency, Currency)

    def test_get_currencies_wrong_id(self):
        result = get_currencies(['KEK'])
        self.assertEqual(len(result), 0)
        
    def test_author_controller(self):
        response = self.author_controller.handle_get('/', params={})
        self.assertIsNotNone(response)
        
        template = self.template_index.render({'app': APP, 'pages': PAGES}).encode()
        self.assertEqual(response.status, HTTPStatus.OK)
        self.assertEqual(response.content, template)
        self.assertEqual(response.headers, {
            'Content-Type': 'text/html',
            'Content-Length': len(template)
        })
        
        response = self.author_controller.handle_get('/author', params={})
        self.assertIsNotNone(response)
        
        template = self.template_author.render({'app': APP, 'pages': PAGES}).encode()
        self.assertEqual(response.status, HTTPStatus.OK)
        self.assertEqual(response.content, template)
        self.assertEqual(response.headers, {
            'Content-Type': 'text/html',
            'Content-Length': len(template)
        })
        
    def test_currencies_controller(self):
        response = self.currencies_controller.handle_get('/currencies', params={})
        self.assertIsNotNone(response)
        
        template = self.template_currencies.render({
            'app': APP,
            'pages': PAGES,
            'currencies': [Currency('1', 'USD', 'Доллар', 75, 1), Currency('2', 'EUR', 'Евро', 90, 1)]
        }).encode()
        
        self.assertEqual(response.status, HTTPStatus.OK)
        self.assertEqual(response.content, template)
        self.assertEqual(response.headers, {
            'Content-Type': 'text/html',
            'Content-Length': len(template)
        })
        
        
        response = self.currencies_controller.handle_get('/currency/delete', params={'id': 1})
        self.assertIsNotNone(response)
        self.assertEqual(response.status, HTTPStatus.OK)
        
        
        response = self.currencies_controller.handle_get('/currency/update', params={'USD': 250})
        self.assertIsNotNone(response)        
        self.assertEqual(response.status, HTTPStatus.OK)
        
        
        self.mock_currencies_db.get_all.assert_called_once()
        self.mock_currencies_db.delete.assert_called_once_with(id=1)
        self.mock_currencies_db.update_by_char_code.assert_called_once_with('USD', 250.0)
        
    def test_users_controller(self):
        response = self.user_controller.handle_get('/users', params={})
        self.assertIsNotNone(response)
        
        template = self.template_users.render({
            'app': APP,
            'pages': PAGES,
            'users': [User(1, "Вася"), User(2, "Петя"), User(3, 'Дима')]
        }).encode()
        
        self.assertEqual(response.status, HTTPStatus.OK)
        self.assertEqual(response.content, template)
        self.assertEqual(response.headers, {
            'Content-Type': 'text/html',
            'Content-Length': len(template)
        })
        
        
        response = self.user_controller.handle_get('/user', params={'id': 1})
        self.assertIsNotNone(response)
        
        template = self.template_user.render({
            'app': APP,
            'pages': PAGES,
            'user': User(1, "Вася"),
            'currencies': [Currency('1', 'USD', 'Доллар', 75, 1)]
        }).encode()
        
        self.assertEqual(response.status, HTTPStatus.OK)
        self.assertEqual(response.content, template)
        self.assertEqual(response.headers, {
            'Content-Type': 'text/html',
            'Content-Length': len(template)
        })
        
        
        self.mock_users_db.get_all.assert_called_once()
        self.mock_users_db.get_by_id.assert_called_once_with(1)

if __name__ == '__main__':
    unittest.main()
