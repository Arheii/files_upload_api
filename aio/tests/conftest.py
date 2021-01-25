import pytest
import shutil
import pathlib
from api.app import init_app


@pytest.fixture
async def client(aiohttp_client):
    '''Run app instanse in temp enviroment'''
    app = init_app()

    app['STORE_DIR'] = app['BASE_DIR'] / 'test_store'
    pathlib.Path.mkdir(app['STORE_DIR'], exist_ok=True)

    # creates TestServer in random unused port
    client = await aiohttp_client(app)
    
    try:
        yield client
    finally:
        shutil.rmtree(app['STORE_DIR'])

