from jinja2.environment import Environment

from utils.response import *
from common import APP, PAGES, Response

from controllers.databaseController import UserDatabase, UserCurrencyDatabase, CurrencyDatabase

class UserController:
    def __init__(self, users_db: UserDatabase, user_currencies_db: UserCurrencyDatabase, currencies_db: CurrencyDatabase, env: Environment):
        self.users_db = users_db
        self.user_currencies_db = user_currencies_db
        self.currencies_db = currencies_db
        self.template_users = env.get_template('users.html')
        self.template_user = env.get_template('user.html')
    
    def handle_get(self, path: str, params: dict) -> Response | None:
        if path == '/users':
            return self._handle_users(params)
        if path == '/user':
            return self._handle_user(params)
        
        return None
    
    def _handle_users(self, params: dict) -> Response:
        users = self.users_db.get_all()
        data = params | {
            'app': APP,
            'pages': PAGES,
            'users': users,
        }
        return Response.html(self.template_users.render(data))
    
    def _handle_user(self, params: dict) -> Response:
        id = params.get('id')
        if id is None:
            return Response.redirect('/users')
        
        try:
            id = int(id)
        except ValueError:
            return Response(HTTPStatus.BAD_REQUEST)
        
        user = self.users_db.get_by_id(int(id))
        if user is None:
            return Response(HTTPStatus.NOT_FOUND)
        
        user_currencies = self.user_currencies_db.get_by_user_id(user.id)
        currencies = map(lambda uc: self.currencies_db.get_by_id(uc.currency_id), user_currencies)
        
        data = params | {
            'app': APP,
            'pages': PAGES,
            'user': user,
            'currencies': currencies
        }
        return Response.html(self.template_user.render(data))