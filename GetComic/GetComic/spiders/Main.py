# -*- coding: utf-8 -*-
import scrapy


class MainSpider(scrapy.Spider):
    name = 'Main'
    allowed_domains = ['manhuadb.com']

    li = ['/manhua/139/1328_13260.html',
 '/manhua/139/1328_13255.html',
 '/manhua/139/1328_13264.html',
 '/manhua/139/1328_13261.html',
 '/manhua/139/1328_13263.html',
 '/manhua/139/1328_13253.html',
 '/manhua/139/1328_13252.html',
 '/manhua/139/1328_13258.html',
 '/manhua/139/1328_13256.html',
 '/manhua/139/1328_13257.html',
 '/manhua/139/1328_13265.html',
 '/manhua/139/1328_13262.html',
 '/manhua/139/1328_13250.html',
 '/manhua/139/1328_13266.html',
 '/manhua/139/1328_13259.html',
 '/manhua/139/1328_13251.html',
 '/manhua/139/1328_13254.html']

    start_urls = []
    for i in li:
        start_urls.append('https://www.manhuadb.com' + i)

    def parse(self, response):

        # pages = response.xpath('//li[@class="sort_div "]/a/@href').getall()

        img_url = response.xpath('//div[@class="text-center"]//img[@class="img-fluid"]/@src').get()

        if img_url != None:

            img_url ='https://www.manhuadb.com' + img_url

            print(img_url)

            yield {
                'url': img_url
            }

            next_url = response.xpath('//a[@class="btn btn-primary mb-1 pnext"][1]/@href').get()

            if next_url != None:

                new_next_url = 'https://www.manhuadb.com' + next_url

                print(new_next_url)

                yield scrapy.Request(
                    new_next_url,
                    self.parse
                )


