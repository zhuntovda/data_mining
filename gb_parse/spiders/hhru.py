import scrapy
from ..loaders import HHVacancyLoader, HHCompanyLoader


class HunterSpider(scrapy.Spider):
    name = 'hhru'
    db_type = 'MONGO'
    allowed_domains = ['hh.ru']
    start_urls = ['https://hh.ru/search/vacancy?schedule=remote&L_profession_id=0&area=1261']
    xpath_build = {
        'pagination': '//div[@data-qa="pager-block"]//a[@data-qa="pager-page"]/@href',
        'vacancy_urls': '//a[@data-qa="vacancy-serp__vacancy-title"]/@href',
    }
    xpath_vacancy = {
        'title': '//h1[@data-qa="vacancy-title"]/text()',
        'salary': '//p[@class="vacancy-salary"]//text()',
        'description': '//div[@data-qa="vacancy-description"]//text()',
        'skills': '//div[@class="bloko-tag-list"]//span[@data-qa="bloko-tag__text"]/text()',
        'company_url': '//a[@data-qa="vacancy-company-name"]/@href',
    }

    xpath_company = {
        'name': '//h1/span[contains(@class, "company-header-title-name")]/text()',
        'url1': '//a[contains(@data-qa, "vacancy-company-name")]/@href',
        'url2': '//div[contains(@class, "vacancy-company-logo")]/a/@href',
        'description': '//div[contains(@data-qa, "company-description")]//text()',
        'site_url': '//a[contains(@data-qa, "sidebar-company-site")]//@href',

    }

    def parse(self, response, **kwargs):
        for pag_page in response.xpath(self.xpath_build['pagination']):
            yield response.follow(pag_page, callback=self.parse)

        for vacancy_page in response.xpath(self.xpath_build['vacancy_urls']):
            yield response.follow(vacancy_page, callback=self.vacancy_parse)

    def vacancy_parse(self, response, **kwargs):
        loader = HHVacancyLoader(response=response)
        loader.add_value('url', response.url)
        for key, value in self.xpath_vacancy.items():
            loader.add_xpath(key, value)

        yield loader.load_item()

        if response.xpath(self.xpath_company['url1']).get():
            yield response.follow(response.xpath(self.xpath_company['url1']).get(), callback=self.company_parse)
        elif response.xpath(self.xpath_company['url2']).get():
            yield response.follow(response.xpath(self.xpath_company['url2']).get(), callback=self.company_parse)

    def company_parse(self, response, **kwargs):
        loader = HHCompanyLoader(response=response)
        loader.add_value('url', response.url)
        loader.add_xpath('name', self.xpath_company['name'])
        loader.add_xpath('description', self.xpath_company['description'])
        loader.add_xpath('site_url', self.xpath_company['site_url'])

        yield loader.load_item()
