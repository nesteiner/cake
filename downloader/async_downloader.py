import asyncio
import aiohttp
import pymongo
import os
client = pymongo.MongoClient()

headers = {
    'Referer': 'https://www.nvshens.org/g/28874/',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'
}

async def fetch(session, url, path):
    async with session.get(url, headers=headers) as resp:
        assert resp.status == 200
        with open(path, 'wb') as f:
            while True:
                chunk = await resp.content.read(10240)
                if not chunk:
                    break
                f.write(chunk)

async def download(storage_path, album):
    # test one album
    async with aiohttp.ClientSession() as session:
        urls = map(lambda image: image['url'], album.find())
        paths = map(lambda image: os.path.join(storage_path, image['filename']), album.find())

        # coros = map(lambda url, path: fetch(session, url, path), urls, paths)
        coros = [fetch(session, url, path) for url, path in zip(urls, paths)]
        await asyncio.wait(coros, return_when = asyncio.tasks.FIRST_EXCEPTION)


        
# sync version: 12.1302 sec
# async version: 0.7

# TODO now download a model
async def download_model(db_name, directory):
    path = os.path.join(directory, db_name)
    db = client[db_name]
    album_names = db.list_collection_names()

    # STUB
    corolst = []
    for album_name in album_names:
        album = db[album_name]
        target_path = os.path.join(path, album_name)
        task = asyncio.create_task(download(target_path, album))
        await task




db_name = 'cake'
directory = os.path.join('/home/steiner/workspace/nc/', db_name)
if not os.path.exists(directory):
    os.makedirs(directory)

import time
start_time = time.time()
asyncio.run(download_model(db_name, directory))
end_time = time.time()
print('Time: ', end_time - start_time)

