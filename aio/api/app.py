"""
Test task for drweb vacancy.
Api for download/upload/delete files
each file saves by its hash instead of name,
by path:  'store/hash[:2]/.
TODO:   Project structure
       python -m aiohttp.web -H localhost -P 8080 api:init_func


"""

import pathlib
from aiohttp import web

from config.settings import config
from .routes import setup_routes


def main():
    app = web.Application(client_max_size=config.pop('client_max_size'))
    app['config'] = config

    app['BASE_DIR'] =  pathlib.Path(__file__).parent.parent
    app['STORE_DIR'] = app['BASE_DIR'] / 'store'

    pathlib.Path.mkdir(app['STORE_DIR'], exist_ok=True)

    setup_routes(app)
    web.run_app(app)


if __name__ == '__main__':
    main(None)