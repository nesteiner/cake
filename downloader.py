import pymongo
import requests
import os
import random
import pdb
from time import sleep
client = pymongo.MongoClient('mongodb://localhost:27017')

cookie = 'Hm_lvt_0f1f5a5e4d9fc6dc0f52ab6f2ec45893=1601958469; gallery_28874=1; gallery_33101=1; records=%5B%7B%22id%22%3A%2221339%22%2C%22name%22%3A%22%u5F90%u5609%u4E50%22%7D%2C%7B%22id%22%3A%2221542%22%2C%22name%22%3A%22Evelyn%u827E%u8389%22%7D%2C%7B%22id%22%3A%2228037%22%2C%22name%22%3A%22%u674E%u4F73%u8513%22%7D%2C%7B%22id%22%3A%2226329%22%2C%22name%22%3A%22%u7EF4%u59AE%u5361%22%7D%2C%7B%22id%22%3A%2227959%22%2C%22name%22%3A%22%u9EC4%u91D1%u5B9D%u513F%22%7D%5D; gallery_33259=1; Hm_lpvt_0f1f5a5e4d9fc6dc0f52ab6f2ec45893=1602219236'

header = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'max-age=0',
    'cookie': cookie,
    'referer': 'https://www.haorenka.org/xiaojiejie',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36'
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
            res = requests.get(url, headers = header)
            for content in res.iter_content(102400):
                f.write(content)

        # print('done')

              
import sys
db_name = sys.argv[1]
path = sys.argv[2]
download_model(db_name, path)
# db = client['cake']
# album = db[db.collection_names()[0]]
# directory = '/home/steiner/workspace/storage'
# download_album(album, directory)
   
