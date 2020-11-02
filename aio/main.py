"""
Test task for drweb vacancy.
Api for download/upload/delete files
each file saves by its hash instead of name,
by path:  'store/hash[:2]/.

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

    return web.json_response({'hash': file_hash}, status=201)


@routes.get('/drweb/aiohttp/storage')
async def storage(request):
    """return file from FS by its hash"""
    # TODO: refactor to middleware
    file_hash = request.rel_url.query.get("hash")

    # Hash is there and contains only correct characters
    if file_hash is None or not file_hash.isalnum():
        raise web.HTTPUnprocessableEntity(text='incorrect hash')

    full_path = UPLOAD_FOLDER / file_hash[:2] / file_hash

    # Check file is exist
    if not full_path.exists():
        raise web.HTTPNotFound(text='hash not found')

    # resp = web.Response
    # resp.headers['Content-Type'] = 'application/octet-stream'

    return web.FileResponse(path=full_path)



@routes.delete('/drweb/aiohttp/storage')
async def delele(request):
    """Delete! file from FS by its hash"""
    # TODO: refactor to middleware
    file_hash = request.rel_url.query.get("hash")

    # Hash is there and contains only correct characters
    if file_hash is None or not file_hash.isalnum():
        raise web.HTTPUnprocessableEntity(text='incorrect hash')

    full_path = UPLOAD_FOLDER / file_hash[:2] / file_hash

    # Check file is exist
    if not full_path.exists():
        raise web.HTTPNotFound(text='hash not found')

    # Delete file
    full_path.unlink(missing_ok=True)

    return web.HTTPNoContent()


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