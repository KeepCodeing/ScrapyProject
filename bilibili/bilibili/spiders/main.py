# -*- coding: utf-8 -*-
import scrapy
from scrapy_redis.spiders import RedisSpider
import json
import time

class MainSpider(RedisSpider):
    name = 'main'
    redis_key = 'bili:bili_key'
    allowed_domains = ['bilibili.com']
    # start_urls = ['http://bilibili.com/']

    def parse(self, response):
        data = json.loads(response.text)['data']['list']
        for i in data:
            item = {}
            mid = str(i['mid'])
            mtime = str(i['mtime'])
            face = str(i['face'])
            item['mid'] = mid
            item['mtime'] = mtime
            item['face'] = face

            yield item
            yield scrapy.Request(
                'https://api.bilibili.com/x/relation/followings?vmid={mid}&pn=1&ps=50&order=desc&jsonp=jsonp'.format(mid=mid),
                self.parse
            )


        time.sleep(5)
