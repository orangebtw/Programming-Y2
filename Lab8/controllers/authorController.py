from utils.response import *

from jinja2.environment import Environment

from common import APP, PAGES, Response

class AuthorController:
    def __init__(self, env: Environment):
        self.template_index = env.get_template("index.html")
        self.template_author = env.get_template("author.html")
    
    def handle_get(self, path: str, params: dict) -> Response | None:
        if path == '/':
            return self._handle_index(params)
        if path == '/author':
            return self._handle_author(params)
        
        return None
    
    def _handle_index(self, params: dict) -> Response:
        data = params | {
            'app': APP,
            'pages': PAGES
        }
        return Response.html(self.template_index.render(data))
    
    def _handle_author(self, params: dict):
        data = params | {
            'app': APP,
            'pages': PAGES
        }
        return Response.html(self.template_author.render(data))