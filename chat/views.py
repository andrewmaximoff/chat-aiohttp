from aiohttp import web

import logging

import aiohttp
import aiohttp_jinja2
from aiohttp import web
from faker import Faker

log = logging.getLogger(__name__)


def get_random_name():
    fake = Faker()
    return fake.name()


class Index(web.View):

    async def get(self):
        ws_current = web.WebSocketResponse()
        ws_ready = ws_current.can_prepare(self.request)
        if not ws_ready.ok:
            return aiohttp_jinja2.render_template('index.html', self.request, {})

        await ws_current.prepare(self.request)

        name = get_random_name()
        log.info('%s joined.', name)

        await ws_current.send_json({'action': 'connect', 'name': name})

        for ws in self.request.app['websockets'].values():
            await ws.send_json({'action': 'join', 'name': name})
        self.request.app['websockets'][name] = ws_current

        while True:
            msg = await ws_current.receive()

            if msg.type == aiohttp.WSMsgType.text:
                for ws in self.request.app['websockets'].values():
                    if ws is not ws_current:
                        await ws.send_json(
                            {'action': 'sent', 'name': name, 'text': msg.data})
            else:
                break

        del self.request.app['websockets'][name]
        log.info('%s disconnected.', name)
        for ws in self.request.app['websockets'].values():
            await ws.send_json({'action': 'disconnect', 'name': name})

        return ws_current


async def status(request):
    return web.Response(text='Status: OK!')
