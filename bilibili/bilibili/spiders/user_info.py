# -*- coding: utf-8 -*-
import scrapy
from scrapy_redis.spiders import RedisSpider
import json
import time
import pymysql


class UserInfoSpider(RedisSpider):
    name = 'get_user_info'
    redis_key = 'bili:user_info'
    allowed_domains = ['bilibili.com']
    def __init__(self):
        self.conn = pymysql.connect(host='192.168.2.170', user='root', password='123456', charset='utf8', port=3306, database='bili_user')
        self.cur = self.conn.cursor()
        self.sql = 'select mid from user_info'
        self.uid_list = []
        for i in range(self.cur.execute(self.sql)):
            self.uid_list.append(self.cur.fetchone())


    def parse(self, response):
        data = json.loads(response.text)['data']
        item = {}
        item['user_name'] = data['name']
        item['sex'] = data['sex']
        item['sign'] = data['sign']
        item['user_level'] = data['level']
        item['birthday'] = data['birthday']
        item['coins'] = str(data['coins'])
        item['vip_type'] = str(data['vip']['type'])
        item['vip_status'] = str(data['vip']['status'])
        yield item

        uids = []
        for i in self.uid_list:
            uids.append(i[0])
            if (len(uids)) % 50 == 0:
                for n in uids:
                    yield scrapy.Request(
                        url='https://api.bilibili.com/x/space/acc/info?mid={uid}&jsonp=jsonp'.format(uid=str(n)),
                        callback=self.parse
                    )
                    time.sleep(2.5)
                uids = []






    def __del__(self):
        self.cur.close()
        self.conn.close()
        pass
