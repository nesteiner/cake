# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
client = pymongo.MongoClient('mongodb://localhost:27017/')
# db = client['MFStar']
class CakePipeline(object):
    def process_item(self, item, spider):
        db_name = spider.db_name
        db = client[db_name]

        album_name = item['name']
        item.pop('name')
        album_collection = db[album_name]
        
        for filename, url in item.items():
            contents = {'filename': filename, 'url': url}
            album_collection.insert_one(contents)
        # with open('/home/steiner/workspace/Nexus/cake/' + album_name, 'w') as f:
        #     for filename, url in item.items():
        #         content = filename + ': ' + url + '\n'
        #         f.write(content)
