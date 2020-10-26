from io import BytesIO
from application import app
import requests

# def test_file_upload():
#     client = app.test_client() # you will need your flask app to create the test_client
#     data = {
#         'file': (BytesIO('my file contents'), 'test_file.txt'), # we use StringIO to simulate file object
#     }
#     # note in that in the previous line you can use 'file' or whatever you want.
#     # flask client checks for the tuple (<FileObject>, <String>)
#     res = client.post("/api/search-objects", data=data)
#     assert res.status_code == 201

def test_via_request():
    