import pymongo
import requests
import os
import random
import pdb
from time import sleep
client = pymongo.MongoClient('mongodb://localhost:27017')

headers = {
    'Referer': 'https://www.nvshens.org/g/28874/',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'
}


def download_model(db_name, path):
    # path: path link to directory download like cake
    # handle path
    if not path.endswith('/'):
        path += '/'

    path += (db_name + '/')
    db = client[db_name]
    album_names = db.collection_names()
    for album_name in album_names:
        album = db[album_name]
        target_path = path + album_name.replace(' ', '') + '/'
        # print('target path: {}'.format(target_path))
        # target_path = path + album_name + '/'
        download_album(album, target_path)

# Description 就一张专辑，别搞错了
def download_album(album, directory):
    if not directory.endswith('/'):
        directory += '/'
        
    if not os.path.exists(directory):
        os.makedirs(directory)
        
    for image in album.find():
        filename = image['filename']
        url = image['url']
        # print('downloading  {} from {}'.format(filename, url))
        path = directory + filename
        with open(path, 'wb') as f:
            # sleep(0.1)
            res = requests.get(url, headers = headers)
            for content in res.iter_content(102400):
                f.write(content)

        # print('done')

              
# import sys
# db_name = sys.argv[1]
# path = sys.argv[2]
# download_model(db_name, path)

# test for one album
db = client['cake']
album_name = db.collection_names()[0]
album = db[album_name]
directory = '/home/steiner/workspace/nc/cake/' + album_name

import time
start_time = time.time()
download_album(album, directory)
end_time = time.time()
print('Time: ', end_time - start_time)
