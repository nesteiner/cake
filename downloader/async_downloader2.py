import aiohttp
import asyncio
import time
import pymongo
import os
client = pymongo.MongoClient()

headers = {
    'Referer': 'http://pic.netbian.com/4kmeinv/index.html',
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

async def download(directory, collection):
    async with aiohttp.ClientSession() as session:
        urls = map(lambda record: record['url'], collection.find())
        filenames = map(lambda record: os.path.join(directory, record['filename']), collection.find())

        coros = map(lambda url, path: fetch(session, url, path), urls, filenames)
        await asyncio.wait(coros)

# Description for 127.75, 87.83
async def main():
    directory1 = '/home/steiner/workspace/nc/images1/'
    directory2 = '/home/steiner/workspace/nc/images2/'
    if not os.path.exists(directory1):
        os.makedirs(directory1)

    if not os.path.exists(directory2):
        os.makedirs(directory2)

    collection = client['async']['storage']

    task1 = asyncio.create_task(download(directory1, collection))
    task2 = asyncio.create_task(download(directory2, collection))

    await task1
    await task2


# Description for 36.61
# async def main():
#     directory = '/home/steiner/workspace/nc/images/'
#     if not os.path.exists(directory):
#         os.makedirs(directory)

#     collection = client['async']['storage']
#     await download(directory, collection)
    


start_time = time.time()
asyncio.run(main())
end_time = time.time()
print('Time: ', end_time - start_time)

# PROBLEM await task or await corotine
# PROBLEM await task which await corotine

import random
async def g(x):
    print(x)
    
async def f():
    coros = [g(x) for x in range(1,3)]
    await asyncio.wait(coros)

async def main():
    task1 = asyncio.create_task(f())
    task2 = asyncio.create_task(f())

    await task1
    await task2
    
asyncio.run(main())
