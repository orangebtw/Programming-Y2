from typing import Iterable
from models.app import App
from models.author import Author

from http import HTTPStatus

APP = App('Актуальные курсы валют', '0.0.1', Author('Карпов Роман', 'ИВТ-2'))
PAGES = (
    {
        'caption': 'Главная',
        'href': '/'
    },
    {
        'caption': 'Курсы',
        'href': '/currencies'
    },
    {
        'caption': 'Пользователи',
        'href': '/users'
    },
    {
        'caption': 'Автор',
        'href': '/author'
    },
)

class Response:
    def __init__(self, status: HTTPStatus, content: bytes | None = None):
        self._status = status
        self._content = content
        self._headers = {}
        
    @staticmethod
    def html(html: str, status: HTTPStatus = HTTPStatus.OK) -> Response:
        content = html.encode()
        return Response(status=status, content=content).with_headers({
            'Content-Type': 'text/html',
            'Content-Length': len(content)
        })
        
    @staticmethod
    def redirect(location: str) -> Response:
        return Response(status=HTTPStatus.MOVED_PERMANENTLY).with_headers({
            'Location': location
        })
    
    def with_headers(self, headers: dict[str, str]) -> Response:
        self._headers.update(headers)
        return self
        
    @property
    def status(self) -> HTTPStatus:
        return self._status
    
    @property
    def content(self) -> bytes | None:
        return self._content
    
    @property
    def headers(self) -> dict[str, str]:
        return self._headers