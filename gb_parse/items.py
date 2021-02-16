# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class GbParseItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class AutoYoulaItem(scrapy.Item):
    _id = scrapy.Field()
    title = scrapy.Field()
    images = scrapy.Field()
    description = scrapy.Field()
    url = scrapy.Field()
    autor = scrapy.Field()
    specifications = scrapy.Field()


class HHVacancyItem(scrapy.Item):
    _id = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    salary = scrapy.Field()
    description = scrapy.Field()
    skills = scrapy.Field()
    company_url = scrapy.Field()


class HHCompanyItem(scrapy.Item):
    _id = scrapy.Field()
    url = scrapy.Field()
    name = scrapy.Field()
    description = scrapy.Field()
    site_url = scrapy.Field()


class Insta(scrapy.Item):
    _id = scrapy.Field()
    date_parse = scrapy.Field()
    data = scrapy.Field()
    img = scrapy.Field()


class InstaUser(Insta):
    _id = scrapy.Field()
    user = scrapy.Field()
    owner = scrapy.Field()
    type_user = 'user'


class InstaFollow(scrapy.Item):
    _id = scrapy.Field()
    owner = scrapy.Field()
    user = scrapy.Field()
    type_user = 'follow'
    # follower_id = scrapy.Field()


class InstaFollower(scrapy.Item):
    _id = scrapy.Field()
    owner = scrapy.Field()
    user = scrapy.Field()
    type_user = 'follower'
    # follower_id = scrapy.Field()
