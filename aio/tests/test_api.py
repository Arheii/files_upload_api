import pytest
import os
import json
import hashlib
from io import BytesIO


async def test_testform(client):
    resp = await client.get('/drweb/aiohttp')

    assert resp.status == 200




