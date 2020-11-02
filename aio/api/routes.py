from .views import StorageView, upload_form
from aiohttp import web


def setup_routes(app):
    app.add_routes([web.view('/drweb/aiohttp/storage', StorageView),
                    web.get('/drweb/aiohttp', upload_form)])


