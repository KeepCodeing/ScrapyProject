# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql


class BilibiliPipeline(object):
    def process_item(self, item, spider):
        if spider.name == 'main':
            insert_get_mid = 'insert into user_info (face, mid, mtime) value ("%s", "%s", "%s")' % (item['face'],
                                                                                                    item['mid'],
                                                                                                    item['mtime'])
            self.cur.execute(insert_get_mid)
        elif spider.name == 'get_user_info':
            insert_get_info = 'insert into main_user_info (user_name, sex, sign, user' \
                              '_level, birthday, coins, vip_type, vip_status) value ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")' % \
                              (item['user_name'], item['sex'], item['sign'], item['user_level'], item['birthday'], item['coins'], item['vip_type'], item['vip_status'])
            self.cur.execute(insert_get_info)
        self.conn.commit()
        return item
    def open_spider(self, spider):

        self.conn = pymysql.connect(host='192.168.2.170', user='root', password='123456', port=3306, charset='utf8', database='bili_user')
        self.cur = self.conn.cursor()
        if spider.name == 'main':
            self.cur.execute('select * from user_info')
            print('*' * 20 + spider.name + '*' * 20)
        elif spider.name == 'get_user_info':
            self.cur.execute('select * from main_user_info')
            print('*'*20+spider.name+'*'*20)


    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()

