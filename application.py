"""
Test task for drweb vacancy.
Api for download/upload/delete files
each file saves by its hash instead of name,
path:  'store/hash[:2]/hash[2:].
Done with jsonapi way
"""

import hashlib
from flask import Flask, jsonify, send_file


app = Flask(__name__)

UPLOAD_FOLDER = os.path.join(app.instance_path, 'store')



app.config['MAX_CONTENT_LENGTH'] = 24 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

print(app.instance_path)

# hashlib.sha224(b'Hello Word1').hexdigest()

@app.route("/drweb/api/files/<string:file_hash>", methods=['GET', 'DELETE'])
def download(file_hash):
    """return or delete file by its hash"""
    full_path = os.path.join(UPLOAD_FOLDER, file_hash[:2], file_hash[2:])

    # Check file is exist
    if not os.path.exists(full_path):
        return jsonify({"error": "file with this hash not found"}), 404

    # Return file
    if request.method == 'GET':
        return send_file(full_path, as_attachment=True)
        # return jsonify({"file": file})

    # Delete file
    if request.method == 'DELETE':
        os.remove(full_path)
         return jsonify({'data':[]}), 204



@app.route("/drweb/api/files", methods=['POST'])
def upload():
    """upload file to server folder (with new name by hash)"""

    try:
        query = request.get_json()
        data = query['data']
    except:
        return jsonify({"error": "incorrect json"}), 422


        filename = hashlib.sha224(b'Hello Word1').hexdigest()

    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename[:2], filename[2:]))




if __name__ == '__main__':
    app.run(debug=True)