# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter


# class ElectronicsPipeline:
#     def process_item(self, item, spider):
#         return item

from itemadapter import ItemAdapter
from pymongo import MongoClient
import pymongo

class ElectronicsPipeline(object):
    def _init_(self, mongo_uri, mongo_db, mongo_coll):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.mongo_coll = mongo_coll

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get("MONGO_URI"),
            mongo_db=crawler.settings.get("MONGO_DATABASE", "ProductDetails"),
            mongo_coll=crawler.settings.get("MONGO_COLL_QUOTES", "electronics"),
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.collection = self.db[self.mongo_coll]

    def close_spider(self, spider):
        self.client.close()
        print('Stored')

    def process_item(self, item, spider):
        item_dict = ItemAdapter(item).asdict()
        self.collection.insert_one(item_dict)
        return item