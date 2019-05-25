# # -*- coding: utf-8 -*-
#
# # Define your item pipelines here
# #
# # Don't forget to add your pipeline to the ITEM_PIPELINES setting
# # See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
# # import pymysql
#
# class NewtiebaspiderPipeline(object):
#
#     def process_item(self, item, spider):
#         sql = 'insert into posts (speaker, content) value ("%s", "%s")' % (item['name'], item['msg'])
#         # print(sql)
#         self.cur.execute(sql)
#         return item
#
#     def open_spider(self, spider):
#         print('*'*10+'Im start now!'+'*'*10)
#
#         self.conn = pymysql.connect(user='root', password='123456', database='tieba', port=3306, host='localhost', charset='utf8')
#         self.cur = self.conn.cursor()
#         self.cur.execute('select * from posts')
#
#     def close_spider(self, spider):
#         print('*'*10+'Im close now!'+'*'*10)
#         self.conn.commit()
#         self.cur.close()
#         self.conn.close()
