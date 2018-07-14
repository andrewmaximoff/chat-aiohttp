import logging

import jinja2
import aiohttp_jinja2

from aiohttp import web

from chat.settings import config
from chat.routes import setup_routes


async def init_app():

    app = web.Application()

    app['config'] = config
    app['websockets'] = {}

    app.on_shutdown.append(shutdown)

    aiohttp_jinja2.setup(
        app, loader=jinja2.PackageLoader('chat', 'templates'))
    app['static_root_url'] = '/chat/static'
    app.router.add_static('/chat/static', 'chat/static', name='static')
    setup_routes(app)

    return app


async def shutdown(app):
    for ws in app['websockets'].values():
        await ws.close()
    app['websockets'].clear()


def main():

    logging.basicConfig(level=logging.DEBUG)

    app = init_app()
    web.run_app(app)


if __name__ == '__main__':
    main()
