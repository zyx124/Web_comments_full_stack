# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import csv
import pymysql
import os
from textblob import TextBlob

# file_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# print(file_path)
dbInfo = {
    'host' : 'localhost',
    'port' : 3306,
    'user' : 'root',
    'password' : 'zhao',
    'db' : 'test'
}

conn = pymysql.connect(
            host = dbInfo["host"],
            port = dbInfo["port"],
            user = dbInfo["user"],
            password = dbInfo["password"],
            db = dbInfo['db'],

        )
cursor = conn.cursor()
cursor.execute("use test")

class NewsPipeline(object):

    def process_item(self, item, spider):
        commentID = item["commentID"] + ""
        comment = item["comment"] + "\n"
        sentiment = TextBlob(comment).sentiment.polarity

        try:
            sql = 'insert into comments (commentId, comment, sentiment) values (%s, %s, %s)'
            cursor.execute(sql, (commentID, comment, sentiment))

            conn.commit()

            # print(os.getcwd())
            # file = open(file_path+"/res.csv", 'a+', newline='')
            # w = csv.writer(file)
            # w.writerow([commentID, comment])
            # file.close()
        except Exception as e:
            print(e)
        return item
