"""
Test task for drweb vacancy.
Api for download/upload/delete files
each file saves by its hash instead of name,
by path:  'store/hash[:2]/.
"""

import os
import hashlib
from flask import Flask, send_file, request, jsonify


app = Flask(__name__)

UPLOAD_FOLDER = os.path.join(app.root_path, 'store')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route("/drweb/api/storage", methods=['POST'])
def upload():
    """Upload file to server folder (with new name by hash), return hash"""

    file = request.files.get('file')
    if file is None:
        return 'file wasn\'t attach', 400

    file_hash = hashlib.sha224(file.read()).hexdigest()
    full_path = os.path.join(UPLOAD_FOLDER, file_hash[:2], file_hash)

    if not os.path.exists(full_path):
        # Create subfolder by first two symbols and save file
        os.makedirs(os.path.join(UPLOAD_FOLDER, file_hash[:2]), exist_ok=True)
        file.seek(0)
        file.save(full_path)

    return jsonify({'hash': file_hash}), 201


@app.route("/drweb/api/storage", methods=['GET', 'DELETE'])
def storage():
    """return or delete file by its hash"""
    file_hash = request.args.get("hash")

    # Hash is there and contains only correct characters
    if file_hash is None or not file_hash.isalnum():
        return 'need correct hash', 422

    full_path = os.path.join(UPLOAD_FOLDER, file_hash[:2], file_hash)

    # Check file is exist
    if not os.path.exists(full_path):
        return "file with this hash not found", 404

    # Return file
    if request.method == 'GET':
        # TODO return filename. ideas - light database. attachment_filename='',
        return send_file(full_path, as_attachment=True)

    # Delete file
    if request.method == 'DELETE':
        os.remove(full_path)
        return '', 204
