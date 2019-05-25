# -*- coding: utf-8 -*-
import scrapy
import json

class TSpider(scrapy.Spider):
    name = 't'
    allowed_domains = ['bilibili.com']
    start_urls = ['https://api.bilibili.com/x/space/acc/info?mid={uid}&jsonp=jsonp'.format(uid=94649037)]

    def __init__(self):
        self.uid =  243821484
        pass
    def parse(self, response):
        item = {
        }
        item['t'] = json.loads(response.text)
        yield item
        yield scrapy.Request(
            url='https://api.bilibili.com/x/space/acc/info?mid={uid}&jsonp=jsonp'.format(uid=self.uid),
            # headers=headers,
            callback=self.parse
        )

    # def start_requests(self):
    #     headers={
    #         'Host': 'api.bilibili.com',
    #         'Origin': 'https://space.bilibili.com',
    #         'Referer': 'https://space.bilibili.com/{uid}'.format(uid=self.uid)
    #     }
    #
    #     url = ['https://api.bilibili.com/x/space/acc/info?mid={uid}&jsonp=jsonp'.format(uid=83853950)]
    #
    #     yield scrapy.Request(
    #         url=url,
    #         headers=headers,
    #         callback=self.parse
    #     )
    #     pass