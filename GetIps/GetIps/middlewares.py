# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

import random
import pymysql

class SetProxy(object):
    def __init__(self):
        self.conn = pymysql.connect(user='root', password='123456', port=3306, host='localhost', database='ips', charset='utf8')
        self.cur = self.conn.cursor()

    def __del__(self):
        self.conn.commit()
        self.cur.close()
        self.conn.close()
        self.count = 1

    def process_rquest(self, spider, request):
        self.cur.execute('select ip from ip_table')

        ip_data = self.cur.fetchall()

        request.meta['proxy'] = str(ip_data[(self.count-1) // 3])

        print('*'*10+'Now IP: %s ' % (str(ip_data[(self.count-1) // 3]), )+ '*'*10)

        self.count += 1

class RandomUa(object):
    def process_request(self, spider, request):

        ua = random.choice(spider.settings.get('USER_AGENTS'))

        request.headers['User-Agent'] = ua


class CheckUa(object):
    def process_response(self, spider, request, response):

        print('*'*10+str(request.headers['User-Agent'])+'*'*10)

        return  response
