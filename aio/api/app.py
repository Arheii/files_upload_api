"""
Test task 
Api for download/upload/delete files
each file saves by its hash instead of name,
by path:  'store/hash[:2]/.

for run:
python -m aiohttp.web -H localhost -P 8080 api:main

"""

import pathlib
from aiohttp import web

from config.settings import config
from .routes import setup_routes


def init_app():
    '''create and prepare app for run'''
    app = web.Application(client_max_size=config.pop('client_max_size'))
    app['config'] = config
  
    app['BASE_DIR'] =  pathlib.Path(__file__).parent.parent
    app['STORE_DIR'] = app['BASE_DIR'] / config.pop('storage_folder')

    setup_routes(app)
    return app


def main(args): 
    app = init_app()
    pathlib.Path.mkdir(app['STORE_DIR'], exist_ok=True)
    
    web.run_app(app)


if __name__ == '__main__':
    main()