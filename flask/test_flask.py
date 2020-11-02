# python -m pytest

import os
import json
import hashlib
from io import BytesIO
from application import app
from werkzeug.datastructures import FileStorage


client = app.test_client()


def upload_file(size=1024):
    """Uploads a randomly generated file to the server via POST
    Uses StringIO to simulate file object"""
    data = {'file': (BytesIO(os.urandom(size)), 'text.txt'), }
    response = client.post("/drweb/api/storage", data=data)
    return response


def test_file_upload():
    """Send 1 file via POST"""
    res = upload_file()
    assert res.status_code == 201


def test_50_uploads():
    """Send 50 files"""
    for _ in range(50):
        res = upload_file()
        assert res.status_code == 201


def test_upload_large_file():
    """File >10mb and check correct hash"""
    path = os.path.join(app.root_path, 'blob.dat')
    big_file = FileStorage(
        stream=open(path, "rb"),
        filename="blob.dat",
        content_type="application/octet-stream",
    ),
    data = {'file': big_file, }
    res = client.post("/drweb/api/storage", data=data)

    with open(path, "rb") as f:
        file_hash = hashlib.sha224(f.read()).hexdigest()

    assert res.status_code == 201
    assert res.json['hash'] == file_hash


def test_too_large_upload():
    """Current max_size for file 32mb"""
    res = upload_file(size=10**8)
    assert res.status_code != 201


def test_download_file():
    """Upload and download back a file from server"""
    hash_file = upload_file().json['hash']
    res = client.get("/drweb/api/storage", query_string={'hash': hash_file})
    assert res.status_code == 200


def test_del_file():
    """Delete existing file"""
    hash_file = upload_file().json['hash']
    res = client.delete("/drweb/api/storage", query_string={'hash': hash_file})
    assert res.status_code == 204

    # Checking the file is deleted
    res = client.get("/drweb/api/storage", query_string={'hash': hash_file})
    assert res.status_code == 404


def test_del_nonexisting_file():
    """Try to delete non-existing file"""
    res = client.delete("/drweb/api/storage", query_string={'hash': 'nope'})
    assert res.status_code == 404


def test_files_are_identical():
    """the file is the same after upload and download"""
    path = os.path.join(app.root_path, 'README.md')
    with open(path, "rb") as f:
        hash_before_send = hashlib.sha224(f.read()).hexdigest()

    # Upload
    file = FileStorage(
        stream=open(path, "rb"),
        filename="readme.md",
        content_type="text/plain",
        ),
    data = {'file': file, }
    res = client.post("/drweb/api/storage", data=data)
    hash_file = res.json['hash']

    # Download
    res = client.get("/drweb/api/storage", query_string={'hash': hash_file})
    file = res.data
    hash_afted_dwnl = hashlib.sha224(file).hexdigest()

    assert hash_before_send == hash_afted_dwnl


if __name__ == '__main__':
    test_files_are_identical()
