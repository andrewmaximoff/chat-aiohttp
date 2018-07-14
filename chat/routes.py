from aiohttp import web

from chat.views import (
    Index, status
)


routes = [
    web.get('/', Index, name='index'),
    web.get('/status', status, name='status'),
]


def setup_routes(app):
    app.router.add_routes(routes)
