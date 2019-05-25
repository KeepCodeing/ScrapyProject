# -*- coding: utf-8 -*-
import scrapy


class IconsSpider(scrapy.Spider):
    name = 'Icons'
    allowed_domains = ['52112.com']
    start_urls = ['https://icon.52112.com/list/118065.html']

    def parse(self, response):

        srcs = response.xpath('//section[@class="icon-items-wra"]//ul[@class="item hasicons"]//li//div[@class="img"]//img[@class="lazy"]//@data-original')

        titles = response.xpath('//section[@class="icon-items-wra"]//ul[@class="item hasicons"]//li//div[@class="img"]//img[@class="lazy"]//@alt')

        download_urls = []

        download_titles = []

        for i in srcs:

            download_urls.append(i.extract())


        for i in titles:

            download_titles.append(i.extract())

        zipped = list(zip(download_titles, download_urls))

        for i in zipped:
            
            yield {
                "title":i[0],
                "src":i[1]
            }

        next_page = response.xpath('//div[@class="pagination"]//a[text()="下一页 >"]/@href').get()

        if next_page != None:

            next_url = 'https://icon.52112.com' + next_page

            print(next_url)

            yield scrapy.Request(
                next_url,
                self.parse
            )




