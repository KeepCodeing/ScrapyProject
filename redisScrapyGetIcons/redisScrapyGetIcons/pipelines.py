# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql

class RedisscrapygeticonsPipeline(object):
    def open_spider(self, spider):
        self.conn = pymysql.connect(host='localhost', password='123456', user='root', database='icons', port=3306, charset='utf8')
        self.cur = self.conn.cursor()
        self.cur.execute('select * from icons_table')
    def close_spider(self, spider):
        self.conn.commit()
        self.cur.close()
        self.conn.close()
    def process_item(self, item, spider):

        sql = 'insert into icons_table (title, url) value ("%s", "%s")' % (item['img_title'], item['img_url'])

        self.cur.execute(sql)
        return item
