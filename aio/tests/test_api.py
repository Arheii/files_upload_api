import pytest
import os
import json
import hashlib
from io import BytesIO


def upload_file(client, size=1024):
    """Uploads a randomly generated file to the server via POST
    Uses StringIO to simulate file object"""
    data = {'file': (BytesIO(os.urandom(size)), 'text.txt'), }
    response = client.post("/drweb/aiohttp/storage", data=data)
    return response


async def test_upload(client):
    """single file"""
    # data = {'file': (BytesIO(os.urandom(size)), 'text.txt'), }
    # response = client.post("/drweb/aiohttp/storage", data=data)
    data = FormData()
    data.add_field('file',
               BytesIO(os.urandom(size)),
               filename='report.xls',
               content_type="application/octet-stream")
    resp = client.post("/drweb/aiohttp/storage", data=data)
    # resp = await upload_file(client)
    assert resp.status == 201


async def test_testform(client):
    """available test form"""
    resp = await client.get('/drweb/aiohttp')

    assert resp.status == 200


async def test_temp_testform(client):
    """available test form"""
    resp = await client.get('/drweb/aiohttp')

    assert resp.status == 200




