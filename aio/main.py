"""
realisation task by flask way
TODO:   Project structure
        python -m aiohttp.web -H localhost -P 8080 main:main


"""
import os
from aiohttp import web
import pathlib

routes = web.RouteTableDef()


@routes.get('/drweb/aiohttp')
async def test_form(request):
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



@routes.get('/drweb/aiohttp/storage')
async def storage(request):
    return web.Response(text="Hello, world")


@routes.post('/drweb/aiohttp/storage')
async def upload(request):
    return web.json_response({'hash': 'file_hash'})


@routes.delete('/drweb/aiohttp/storage')
async def delele(request):
    data = {'some': 'data'}
    return web.json_response(data)


# async def store_mp3_handler(request):

#     reader = await request.multipart()

#     # /!\ Don't forget to validate your inputs /!\

#     # reader.next() will `yield` the fields of your form

#     field = await reader.next()
#     assert field.name == 'name'
#     name = await field.read(decode=True)

#     field = await reader.next()
#     assert field.name == 'mp3'
#     filename = field.filename
#     # You cannot rely on Content-Length if transfer is chunked.
#     size = 0
#     with open(os.path.join('/spool/yarrr-media/mp3/', filename), 'wb') as f:
#         while True:
#             chunk = await field.read_chunk()  # 8192 bytes by default.
#             if not chunk:
#                 break
#             size += len(chunk)
#             f.write(chunk)

#     return web.Response(text='{} sized of {} successfully stored'
#                              ''.format(filename, size))

def main(argv):
    PROJ_ROOT = pathlib.Path(__file__).parent

    UPLOAD_FOLDER = PROJ_ROOT / 'store'
    pathlib.Path.mkdir(UPLOAD_FOLDER, exist_ok=True)

    app = web.Application()
    app.add_routes(routes)
    web.run_app(app)


if __name__ == '__main__':
    main(None)