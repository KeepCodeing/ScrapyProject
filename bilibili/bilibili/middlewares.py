# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

import random
import pymysql
import time


class SetProxy(object):
    def __init__(self):
        self.conn = pymysql.connect(user='root', password='123456', port=3306, host='192.168.2.170', database='ips', charset='utf8')
        self.cur = self.conn.cursor()

    def __del__(self):

        self.cur.close()
        self.conn.close()

    def process_request(self, spider, request):
        self.cur.execute('select ip from ip_table')

        ip_data = self.cur.fetchall()

        # while True:
        for i in ip_data:
            request.meta['proxy'] = "http://" + i[0] + ":80"

            print(request.meta['proxy'])
            # print(request.meta['proxy'])
            time.sleep(3)

        #
        # request.meta['proxy'] = str(ip_data[(self.count-1) // 3])
        #
        # print('*'*10+'Now IP: %s ' % (str(ip_data[(self.count-1) // 3]), )+ '*'*10)
        #
        # self.count += 1

class RandomUa(object):
    def process_request(self, spider, request):

        ua = random.choice(spider.settings.get('USER_AGENTS'))

        request.headers['User-Agent'] = ua


class CheckUa(object):
    def process_response(self, spider, request, response):

        print('*'*10+str(request.headers['User-Agent'])+'*'*10)

        return  response
