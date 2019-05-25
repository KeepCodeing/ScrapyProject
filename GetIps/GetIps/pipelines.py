# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
import requests

class GetipsPipeline(object):
    def __init__(self):
        self.conn = pymysql.connect(user='root', password='123456', host='localhost', port=3306, database='ips', charset='utf8')
        self.cur = self.conn.cursor()
        self.cur.execute('select * from xici_ip')

    def __del__(self):
        self.conn.commit()
        self.cur.close()
        self.conn.close()

    def process_item(self, item, spider):

        sql = 'insert into xici_ip (ip_type, ip, ip_port) value ("%s", "%s", "%s")' % (item['type'], item['ip'], item['port'])

        self.cur.execute(sql)

        print(item)

        return item
