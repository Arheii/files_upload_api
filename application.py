"""
Test task for drweb vacancy.
Api for download/upload/delete files
each file saves by its hash instead of name,
by path:  'store/hash[:2]/.
"""

import os
import hashlib
from helper import generate_checksum
from flask import Flask, send_file, request, render_template


app = Flask(__name__)

UPLOAD_FOLDER = os.path.join(app.root_path, 'store')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route("/drweb/api/storage", methods=['POST'])
def upload():
    """Upload file to server folder (with new name by hash), return hash"""

    # Accessing the parses the input stream
    # looks good, but each time got a new hash :(
    # docs: https://flask.palletsprojects.com/en/1.1.x/patterns/requestchecksum/
    # stream_hash = generate_checksum(request)
    # file = request.files
    # file_hash = stream_hash.hexdigest()

    file = request.files.get('file')
    if file is None:
        return 'file wasn\'t attach', 400

    file_hash = hashlib.sha224(file.read()).hexdigest()
    full_path = os.path.join(UPLOAD_FOLDER, file_hash[:2], file_hash)

    if not os.path.exists(full_path):
        # Create subfolder by first two symbols and save file
        os.makedirs(os.path.join(UPLOAD_FOLDER, file_hash[:2]), exist_ok=True)
        file.save(full_path)

    return f'{file_hash}', 201


@app.route("/drweb/api/storage", methods=['GET', 'DELETE'])
def storage():
    """return or delete file by its hash"""


    file_hash = request.args.get("hash")
    if file_hash is None:
        return 'need hash', 422

    full_path = os.path.join(UPLOAD_FOLDER, file_hash[:2], file_hash)

    # Check file is exist
    if not os.path.exists(full_path):
        return "file with this hash not found", 404

    # Return file
    if request.method == 'GET':
        # TODO return filename. idea - light database. attachment_filename='',
        return send_file(full_path, as_attachment=True)

    # Delete file
    if request.method == 'DELETE':
        os.remove(full_path)
        return '', 204






# TODO DEL:
@app.route("/drweb/api/upload_page", methods=['GET'])
def for_test_upload():
    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True)