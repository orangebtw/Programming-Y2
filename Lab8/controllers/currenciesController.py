from jinja2.environment import Environment

from utils.response import *

from controllers.databaseController import CurrencyDatabase

from common import APP, PAGES, Response

class CurrenciesController:
    def __init__(self, db: CurrencyDatabase, env: Environment):
        self.db = db
        self.template_currencies = env.get_template('currencies.html')
    
    def handle_get(self, path: str, params: dict) -> Response | None:
        if path == '/currencies':
            return self._handle_currencies(params)
        if path == '/currency/delete':
            return self._handle_delete(params)
        if path == '/currency/update':
            return self._handle_update(params)
        if path == '/currency/show':
            return self._handle_show()
        
        return None
    
    def _handle_currencies(self, params: dict) -> Response:
        currencies = self.db.get_all()
        data = params | {
            'app': APP,
            'pages': PAGES,
            'currencies': currencies,
        }
        return Response.html(self.template_currencies.render(data))
        
    def _handle_delete(self, params: dict):
        id = params.get('id')
        if id is None:
            return Response(HTTPStatus.BAD_REQUEST)
            
        try:
            id = int(id)
        except ValueError:
            return Response(HTTPStatus.BAD_REQUEST)
    
        self.db.delete(id=id)
        return Response(HTTPStatus.OK)
    
    def _handle_update(self, params: dict):
        for char_code, value in params.items():
            try:
                value = float(value)
            except ValueError:
                continue
            self.db.update_by_char_code(char_code, value)
        return Response(HTTPStatus.OK)
    
    def _handle_show(self):
        currencies = self.db.get_all()
        for currency in currencies:
            print(currency)
        return Response(HTTPStatus.OK)