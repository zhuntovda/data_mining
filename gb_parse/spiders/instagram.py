import datetime as dt
import json
import scrapy
from ..items import InstaUser, InstaFollow, InstaFollower
from ..loaders import InstaLoaderFollow, InstaLoaderFollower


class InstagramSpider(scrapy.Spider):
    name = 'instagram'
    db_type = 'MONGO'
    allowed_domains = ['www.instagram.com']
    start_urls = ['https://www.instagram.com/']
    login_url = 'https://www.instagram.com/accounts/login/ajax/'
    api_url = '/graphql/query/'
    query_hash = {
        'follow': 'd04b0a864b4b54837c0d870b0e77e076',
        'followers': 'c76146de99bb02f6415203be841dd25a'
    }

    def __init__(self, login, enc_password, *args, **kwargs):
        self.users1 = 'polkovnikpowder'
        self.users2 = 'pelevin85'
        self.users_list = []
        self.login = login
        self.enc_password = enc_password
        self.stop = False
        super().__init__(*args, **kwargs)

    def parse(self, response, **kwargs):
        try:
            js_data = self.js_data_extract(response)
            yield scrapy.FormRequest(
                self.login_url,
                method='POST',
                callback=self.parse,
                formdata={
                    'username': self.login,
                    'enc_password': self.enc_password,
                },
                headers={'X-CSRFToken': js_data['config']['csrf_token']}
            )
        except AttributeError as e:
            if response.json().get('authenticated'):
                yield response.follow(f'/{self.users1}/', callback=self.user_page_parse_1, cb_kwargs={'user': self.users1})

    def user_page_parse_1(self, response, user):
        user_data = self.js_data_extract(response)['entry_data']['ProfilePage'][0]['graphql']['user']
        # yield InstaUser(
        #    user=user_data['username'],
        #    owner=user
        # )

        yield from self.get_api_follow_request(response, user_data, user)

    def user_page_parse(self, response):
        if len(self.users_list) != 0:
            yield response.follow(f'/{self.users_list[0]}/', callback=self.user_page_parse_1, cb_kwargs={'user': self.users_list.pop(0)})

    def get_api_follow_request(self, response, user_data, owner, variables=None):
        if not variables:
            variables = {
                'id': user_data['id'],
                'first': 100,
            }
        url = f'{self.api_url}?query_hash={self.query_hash["follow"]}&variables={json.dumps(variables)}'
        yield response.follow(url, callback=self.get_api_follow, cb_kwargs={'user_data': user_data, 'owner': owner})

    def get_api_followers_request(self, response, user_data, owner, variables=None):
        if not variables:
            variables = {
                'id': user_data['id'],
                'first': 100,
            }
        url = f'{self.api_url}?query_hash={self.query_hash["followers"]}&variables={json.dumps(variables)}'
        yield response.follow(url, callback=self.get_api_followers, cb_kwargs={'user_data': user_data, 'owner': owner})

    def get_api_follow(self, response, user_data, owner):
        if b'application/json' in response.headers['Content-Type']:
            data = response.json()
            yield from self.get_follow_item(response, owner, data['data']['user']['edge_follow']['edges'], None)
            if data['data']['user']['edge_follow']['page_info']['has_next_page']:
                variables = {
                    'id': user_data['id'],
                    'first': 100,
                    'after': data['data']['user']['edge_follow']['page_info']['end_cursor'],
                }
                yield from self.get_api_follow_request(response, user_data, owner, variables)
            else:
                yield from self.get_api_followers_request(response, user_data, owner)

    def get_api_followers(self, response, user_data, owner):
        if b'application/json' in response.headers['Content-Type']:
            data = response.json()
            yield from self.get_follow_item(response, owner, None, data['data']['user']['edge_followed_by']['edges'])
            if data['data']['user']['edge_followed_by']['page_info']['has_next_page']:
                variables = {
                    'id': user_data['id'],
                    'first': 100,
                    'after': data['data']['user']['edge_followed_by']['page_info']['end_cursor'],
                }
                yield from self.get_api_follow_request(response, user_data, owner, variables)

    def get_follow_item(self, response, owner, follow_users_data, follower_users_data):

        if follow_users_data:
            for user in follow_users_data:
                yield InstaFollow(
                    user=user['node']['username'],
                    owner=owner
                )

        if follower_users_data:
            for user in follower_users_data:
                yield InstaFollower(
                    user=user['node']['username'],
                    owner=owner
                 )
                yield from self.user_page_parse(response)

    @staticmethod
    def js_data_extract(response):
        script = response.xpath('//script[contains(text(), "window._sharedData =")]/text()').get()
        return json.loads(script.replace("window._sharedData =", '')[:-1])
