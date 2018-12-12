# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sqlite3

class ShuilinewsPipeline(object):
    def open_spider(self,spider):
        self.con=sqlite3.connect('shuili.sqlite')
        self.cu=self.con.cursor()

    def process_item(self, item, spider):
        print(spider.name, 'pipelines')
        insert_sql = "insert into shuili (type,title, url, news_date) values('{}','{}','{}','{}')"\
            .format(item['type'], item['title'], item['url'], item['news_date'])
        print(insert_sql)
        self.cu.execute(insert_sql)  # execute后面接sql语句
        self.con.commit()  # 提交至数据库
        return item

    def spider_close(self, spider):
        self.con.close()  # 关闭数据库连接

