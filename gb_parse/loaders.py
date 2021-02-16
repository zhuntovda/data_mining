import re
from scrapy import Selector
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose
from .items import AutoYoulaItem, HHVacancyItem, HHCompanyItem, InstaFollow, InstaFollower


def get_autor(js_string):
    re_str = re.compile(r"youlaId%22%2C%22([0-9|a-zA-Z]+)%22%2C%22avatar")
    result = re.findall(re_str, js_string)
    return f'https://youla.ru/user/{result[0]}' if result else None


def get_specifications(itm):
    tag = Selector(text=itm)
    result = {tag.css('.AdvertSpecs_label__2JHnS::text').get(): tag.css(
        '.AdvertSpecs_data__xK2Qx::text').get() or tag.css('a::text').get()}
    return result


def specifications_out(data: list):
    result = {}
    for itm in data:
        result.update(itm)
    return result


class AutoYoulaLoader(ItemLoader):
    default_item_class = AutoYoulaItem
    title_out = TakeFirst()
    url_out = TakeFirst()
    description_out = TakeFirst()
    autor_in = MapCompose(get_autor)
    autor_out = TakeFirst()
    specifications_in = MapCompose(get_specifications)
    specifications_out = specifications_out


class HHVacancyLoader(ItemLoader):
    default_item_class = HHVacancyItem
    title_out = TakeFirst()
    url_out = TakeFirst()
    description_in = ''.join
    description_out = TakeFirst()
    salary_in = ''.join
    salary_out = TakeFirst()


class HHCompanyLoader(ItemLoader):
    default_item_class = HHCompanyItem
    name_out = TakeFirst()
    url_out = TakeFirst()
    description_in = ''.join
    description_out = TakeFirst()
    site_url = TakeFirst()


class InstaLoaderFollow(ItemLoader):
    default_item_class = InstaFollow
    date_parse = TakeFirst()
    user_name = TakeFirst()
    user_id = TakeFirst()
    follow_name = TakeFirst()
    follow_id = TakeFirst()


class InstaLoaderFollower(ItemLoader):
    default_item_class = InstaFollower
    date_parse = TakeFirst()
    user_name = TakeFirst()
    user_id = TakeFirst()
    follow_name = TakeFirst()
    follow_id = TakeFirst()