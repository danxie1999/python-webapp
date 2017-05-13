import logging; logging.basciConfig(level=logging.INFO)

import asyncio,os,json,time

from datetime import datetime

from aiohttp import web

def index(request):
	return web.Response(body=b'<h1>Awesome</h1>')

async def init(loop):
	app=Web.Application(loop=loop)
	app.router.add_route('GET','/',index)
	srv = await loop.create_server(app.make_handler(),'127.0.0.1',9999)
	return srv

loop=asyncio.get_event_loop()
loop.run_until_complete(init(loop))
loop.run_forever()