import os
from io import BytesIO
from application import app
from werkzeug.datastructures import FileStorage
import hashlib

def test_file_upload():
    client = app.test_client() # you will need your flask app to create the test_client
    data = {
        'file': (BytesIO(b'my file con tents'), 'test_file.txt'), # we use StringIO to simulate file object
    }
    # note in that in the previous line you can use 'file' or whatever you want.
    # flask client checks for the tuple (<FileObject>, <String>)
    res = client.post("/drweb/api/storage", data=data)
    print(res.data)
    print(hashlib.sha224(BytesIO(b'my file con tents')))
    assert res.status_code == 201

    # big_file = os.path.join(app.root_path, 'blob.dat')
    # big_file = FileStorage(
    #     stream=open(big_file, "rb"),
    #     filename="blob.dat",
    #     content_type="application/octet-stream",
    # ),
    # data = {
    #     'file': big_file,
    # }
    # res = client.post("/drweb/api/storage", data=data)
    # print(res)
    # print(big_file)
    # assert res.status_code == 201

    # file_hash = hashlib.sha224(big_file.stream.read()).hexdigest()



if __name__ == '__main__':
    test_file_upload()
