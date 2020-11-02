"""
realisation task by flask way
TODO:   Project structure
        python -m aiohttp.web -H localhost -P 8080 main:main


"""
import pathlib
import hashlib
from aiohttp import web


PROJ_ROOT = pathlib.Path(__file__).parent
UPLOAD_FOLDER = PROJ_ROOT / 'store'
pathlib.Path.mkdir(UPLOAD_FOLDER, exist_ok=True)

routes = web.RouteTableDef()


@routes.post('/drweb/aiohttp/storage')
async def upload(request):
    """Upload file from post to server folder"""
    # TODO: request.post() -> request.multipart()
    data = await request.post()
    attach = data.get('file')

    if attach is None:
        raise web.HTTPBadRequest(text='no file')

    # filename = attach.filename
    file = attach.file

    file_hash = hashlib.sha224(file.read()).hexdigest()
    full_path = UPLOAD_FOLDER / file_hash[:2] / file_hash

    if not full_path.exists():
        # Create subfolder by first two symbols and save file
        pathlib.Path.mkdir(UPLOAD_FOLDER / file_hash[:2], exist_ok=True)
        file.seek(0)
        # TODO: async file saving
        with open(full_path, 'wb') as f:
            f.write(file.read())

    return web.json_response({'hash': file_hash})


@routes.get('/drweb/aiohttp/storage')
async def storage(request):
    """return or delete file by its hash"""
    file_hash = request.args.get("hash")

    # Hash is there and contains only correct characters
    if file_hash is None or not file_hash.isalnum():
        return 'need correct hash', 422

    full_path = os.path.join(UPLOAD_FOLDER, file_hash[:2], file_hash)

    # Check file is exist
    if not os.path.exists(full_path):
        return "file with this hash not found", 404
        
    return web.Response(text="Hello, world")



@routes.delete('/drweb/aiohttp/storage')
async def delele(request):
    data = {'some': 'data'}
    return web.json_response(data)


@routes.get('/drweb/aiohttp')
async def test_form(request):
    """For testing post query"""
    return web.Response(text="""
                        <!doctype html>
                        <title>Upload new File</title>
                        <h1>Upload new File</h1>
                        <form method=post
                                enctype=multipart/form-data
                                action='/drweb/aiohttp/storage'>
                          <input type=file name=file>
                          <input type=submit value=Upload>
                        </form>
                        """,
                        content_type='text/html')


def main(argv):


    app = web.Application()
    app.add_routes(routes)
    web.run_app(app)


if __name__ == '__main__':
    main(None)