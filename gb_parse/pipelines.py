# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

from itemadapter import ItemAdapter
from itemadapter import ItemAdapter
from scrapy import Request
from scrapy.pipelines.images import ImagesPipeline
from pymongo import MongoClient

class GbParsePipeline:
    def __init__(self):
        self.db = MongoClient()['parse_user_inst']

    def process_item(self, item, spider):
        if spider.stop:
            pass
        elif spider.db_type == 'MONGO':
            if type(item) == dict:
                collection = self.db['InstaUser']
                collection.insert_one(item)
            elif item.type_user == 'follow':
                collection = self.db['InstaFollow']
                collection.insert_one(item)
            elif item.type_user == 'follower':
                collection = self.db['InstaFollower']
                collection.insert_one(item)
                self.add_owners(spider, item)
        return item

    def add_owners(self, spider, item):

        if spider.stop:
            return

        for i in self.db['InstaFollow'].find({'owner': item['owner'], 'user': item['user']}):
            if spider.users2 == i['user']:
                spider.stop = True
                self.how_many_owner(self, spider, item['owner'])
            else:
                if self.db['InstaUser'].find({'user': item['user']}).count() == 0:
                    self.process_item({'type_user': 'user', 'user': item['user'], 'owner': item['owner']}, spider)
                    spider.users_list.append(item['user'])

    def how_many_owner(self, spider, owner):
        self.step_find_owner(self, spider, owner, 1)

    def step_find_owner(self, spider, owner, n):
        for i in self.db['InstaFollow'].find({'user': owner}):
            if spider.users1 == i['owner']:
                print(f'между пользователями {spider.users1} и {spider.users2} рукопожатий {n}')
            else:
                m = n+1
                self.step_find_owner(self, spider, i['owner'], m)




