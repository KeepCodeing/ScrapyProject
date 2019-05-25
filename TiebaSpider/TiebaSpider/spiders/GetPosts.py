# -*- coding: utf-8 -*-
import scrapy
import re

class GetpostsSpider(scrapy.Spider):

    name = 'GetPosts'
    allowed_domains = ['baidu.com']
    start_urls = ['http://tieba.baidu.com/p/6113801159']

    def parse(self, response):

        div_content = response.xpath('//div[@id="j_p_postlist"]')


        name = div_content.xpath('//li[@class="d_name"]/a').extract()
        content = div_content.xpath('//div[@class="d_post_content j_d_post_content  clearfix"]').extract()

        final_content = []
        final_speaker = []

        for n in content:
            t_str = n[n.index('>') + 1:-6]
            c = re.compile('.*(<img .*>).*')
            l = ''
            try:
                l = re.match(c, t_str).group(1)
            except:
                pass

            final_content.append(t_str.replace(l, '').replace(' ','').replace('<br>', ''))


        for i in name:

            a_str = i[i.index('>')+1:-4]
            c = re.compile('.*(<img .*>).*')
            l = ''
            try:
                l = re.match(c, a_str).group(1)
            except:
                pass
            final_speaker.append(a_str.replace(l, ''))

        zipped = list(zip(final_speaker, final_content))

        for i in zipped:
            yield {
                "speaker":i[0],
                "content":i[1]
            }


        next_url = response.xpath('//li[@class="l_pager pager_theme_4 pb_list_pager"]//a[text()="下一页"]/@href')


        if next_url.extract_first() != None:
            new_url = 'http://tieba.baidu.com' + next_url.extract_first()
            print(new_url)
            yield scrapy.Request(new_url)
















