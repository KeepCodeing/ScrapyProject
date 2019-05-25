# -*- coding: utf-8 -*-
import scrapy
from scrapy_redis.spiders import RedisSpider

class IconsSpider(RedisSpider):
    name = 'icons'
    allowed_domains = ['52112.com']
    redis_key = 'icons:geticons'
    # start_urls = ['https://icon.52112.com/list/']
    # https://icon.52112.com/list/

    def parse(self, response):
        next_url = response.xpath('//div[@class="pagination"]/a[text()="下一页 >"]/@href').get()

        if next_url is not None:
            next_url = 'https://icon.52112.com' + next_url

            print('*' * 10 + next_url + '*' * 10)
            yield scrapy.Request(
                url=next_url,
                callback=self.parse
            )

        ul = response.xpath('//ul[@class="item hasicons"]/li[not(@class="lis-none")]/div[@class="img"]')
        for li in ul:
            item = {}
            img_url = li.xpath('img/@src').get()
            img_title = li.xpath('img/@alt').get()

            item['img_url'] = img_url
            item['img_title'] = img_title

            yield item




