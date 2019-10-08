import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem

import sqlite3

class Foussier_Database(object):

    def __init__(self):

        self.create_connection()
        self.create_table()
        pass

    def create_connection(self):

        self.conn = sqlite3.Connection('foussier.db')
        self.curr = self.conn.cursor()
    
    def create_table(self):

        self.curr.execute("drop table if exists foussier_table")
        self.curr.execute("CREATE TABLE foussier_table( sku int, title text, description text, url text )")

    def process_item(self, item, spider):

        self.store_db(item)

        return item

    def store_db(self,item):

        self.curr.execute(f"insert into foussier_table values ({item['sku']},'{item['title']}','{item['description']}','{item['url']}')")

        self.conn.commit()

class FoussierPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):       
        count = 0
        for img_url in item['image_urls']:
            count += 1
            yield scrapy.Request(img_url, meta={'image_name': item["sku"],'count': count})

    def file_path(self, request, response=None, info=None):
        return f"{request.meta['image_name']}_{request.meta['count']}.jpg" 

class DuplicatesPipeline(object):

    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        if item['sku'] in self.ids_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.ids_seen.add(item['sku'])
            return item

