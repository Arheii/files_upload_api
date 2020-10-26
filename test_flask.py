# python -m pytest

import os
import json
import hashlib
from io import BytesIO
from application import app
from werkzeug.datastructures import FileStorage


hashes = []
client = app.test_client()


def test_file_upload():
    """Use StringIO to simulate file object"""
    data = {'file': (BytesIO(b'contents'), 'test.txt'),}
    res = client.post("/drweb/api/storage", data=data)

    assert res.status_code == 201
    hashes.append(res.json['hash'])


def test_50_uploads():
    """Random array bytes"""
    for _ in range(50):
        data = {'file': (BytesIO(os.urandom(30)), 'bytes.dat'),}
        res = client.post("/drweb/api/storage", data=data)
        assert res.status_code == 201


def test_upload_large_file():
    """File >10mb and check correct hash"""
    path = os.path.join(app.root_path, 'blob.dat')
    big_file = FileStorage(
        stream=open(path, "rb"),
        filename="blob.dat",
        content_type="application/octet-stream",
    ),
    data = {'file': big_file,}
    res = client.post("/drweb/api/storage", data=data)

    assert res.status_code == 201

    with open(path, "rb") as f:
        file_hash = hashlib.sha224(f.read()).hexdigest()

    assert res.json['hash'] == file_hash
    hashes.append(res.json['hash'])


def test_download_files():
    for hash_file in hashes:
        res = client.get("/drweb/api/storage", query_string={'hash':hash_file})
        assert res.status_code == 200


def test_delete_file():
    res = client.delete("/drweb/api/storage", query_string={'hash':hashes[0]})
    assert res.status_code == 204

    res = client.get("/drweb/api/storage", query_string={'hash':hashes[0]})
    assert res.status_code == 404

