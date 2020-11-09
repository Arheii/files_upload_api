import hashlib
import pathlib
from aiohttp import web


class StorageView(web.View):
    '''incomplit crud for storage'''
    # TODO:
    # self.store_dir = self.request.config_dict['STORE_DIR']

    async def post(self):
        """Upload file via post to server folder"""
        # TODO: request.post() -> request.multipart()
        data = await self.request.post()
        attach = data.get('file')

        if attach is None:
            raise web.HTTPBadRequest(text='no file')

        # filename = attach.filename
        file = attach.file

        file_hash = hashlib.sha224(file.read()).hexdigest()
        store_dir = self.request.config_dict['STORE_DIR']
        full_path = store_dir / file_hash[:2] / file_hash
        print(full_path)

        if not full_path.exists():
            # Create subfolder by first two symbols and save file
            pathlib.Path.mkdir(store_dir / file_hash[:2], exist_ok=True)
            file.seek(0)
            # TODO: async file saving
            with open(full_path, 'wb') as f:
                f.write(file.read())

        return web.json_response({'hash': file_hash}, status=201)


    async def get(self):
        """return file from FS by its hash"""
        # TODO: refactor to middleware
        file_hash = self.request.rel_url.query.get("hash")


        # Hash is there and contains only correct characters
        if file_hash is None or not file_hash.isalnum():
            raise web.HTTPUnprocessableEntity(text='incorrect hash')

        store_dir = self.request.config_dict['STORE_DIR']
        full_path = store_dir / file_hash[:2] / file_hash

        # Check file is exist
        if not full_path.exists():
            raise web.HTTPNotFound(text='hash not found')

        return web.FileResponse(path=full_path)


    async def delele(self):
        """Delete! file from FS by its hash"""
        # TODO: refactor to middleware
        file_hash = self.request.rel_url.query.get("hash")

        # Hash is there and contains only correct characters
        if file_hash is None or not file_hash.isalnum():
            raise web.HTTPUnprocessableEntity(text='incorrect hash')

        store_dir = self.request.config_dict['STORE_DIR']
        full_path = store_dir / file_hash[:2] / file_hash

        # Check file is exist
        if not full_path.exists():
            raise web.HTTPNotFound(text='hash not found')

        # Delete file
        full_path.unlink(missing_ok=True)

        return web.HTTPNoContent()


# TODO: can be removed
async def upload_form(request):
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
