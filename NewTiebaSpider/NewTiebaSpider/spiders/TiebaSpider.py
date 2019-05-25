# -*- coding: utf-8 -*-
import scrapy
import re
import urllib.parse

class TiebaspiderSpider(scrapy.Spider):
    name = 'TiebaSpider'
    allowed_domains = ['baidu.com']
    baming = input('输入吧名:')
    start_urls = ['http://tieba.baidu.com/f?kw={name}&ie=utf-8&pn=0'.format(name=baming)]

    def parse(self, response):

        mate_url = 'http://tieba.baidu.com/'

        next_page_url = re.findall('<a href="(.+?)".+?>下一页&gt;<.+?>', response.text)[0]

        if int(re.findall('.*?=(\d+)', next_page_url)[0]) <= 50*10-50:

            # print('*'*10+next_page_url+'*'*10)

            base_url = 'http://tieba.baidu.com/f?kw=%E7%9C%9F%E5%A4%8F%E5%A4%9C%E7%9A%84%E9%93%B6%E6%A2%A6&ie=utf-8&pn=0'

            new_url = urllib.parse.urljoin(base_url, next_page_url).replace('amp;', '')

            for url in re.findall('/p/\d+', response.text):

                next_url = urllib.parse.urljoin(mate_url, url)
                # print(next_url)
                yield scrapy.Request(next_url, callback=self.parse_post)

            print('*'*10+new_url+'*'*10)

            if next_page_url != None:

                yield scrapy.Request(
                    new_url,
                    self.parse
                )

    def parse_post(self, response):
        item = {}
        # //div[@id="j_p_postlist"]//div[not(@ad-dom-img="true")]//li[@class="d_name"]/a[not(@class="p_author_name j_click_stats")]/text()
        name = response.xpath('//div[@id="j_p_postlist"]//div[not(@ad-dom-img="true")]//li[@class="d_name"]/a[not(@class="p_author_name j_click_stats")]/text()').getall()

        title = response.xpath('//h1[@class="core_title_txt  "]/text()').get()

        content_t = response.xpath('//div[@id="j_p_postlist"]/div[not(@ad-dom-img="true")]//div[@class="d_post_content j_d_post_content  clearfix"]')
        # //a[@class="j_click_stats"]
        content = []

        next_url = response.xpath('//li[@class="l_pager pager_theme_4 pb_list_pager"]//a[text()="下一页"]/@href').get()

        if next_url != None:

            new_url = 'http://tieba.baidu.com/' + next_url

            print('*'*10+new_url+'*'*10)

            for i in content_t:
                c = i.xpath('text()').getall()
                temp = ''
                for n in c:
                    temp += n

                content.append(temp.replace(' ', ''))

            print('*'*10+str(len(content)), str(len(name)), end='*'*10+'\n')

            zipped = list(zip(name, content))

            # if title != None:
            #     yield {
            #         'title': title,
            #     }
            # else:
            #
            #     title = 'Null'

            print('*'*10+str(title)+'*'*10)

            for i in range(len(zipped)):

                item['name'] = zipped[i][0]
                item['msg'] = zipped[i][1]

                yield item

                # yield {
                #     'name':zipped[i][0],
                #     'msg':zipped[i][1]
                # }

            yield scrapy.Request(
                new_url,
                self.parse_post
            )




