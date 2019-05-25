# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class IpsSpider(scrapy.Spider):
    name = 'Ips'
    allowed_domains = ['xicidaili.com']
    start_urls = ['https://www.xicidaili.com/nn/']

    # rules = (
    #     Rule(LinkExtractor(allow=r'/nn/\d+'), callback='parse_item', follow=True),
    # )

    def parse_item(self, response):
        item = {}

        IPs = response.xpath('//tr[@class="odd"or@class=""]//td[2]/text()').getall()
        Ports = response.xpath('//tr[@class="odd"or@class=""]//td[3]/text()').getall()
        Types = response.xpath('//tr[@class="odd"or@class=""]//td[6]/text()').getall()


        zipped = zip(IPs, Ports, Types)

        for i in list(zipped):

            item['ip'] = i[0]
            item['port'] = i[1]
            item['type'] = i[2]

            yield item