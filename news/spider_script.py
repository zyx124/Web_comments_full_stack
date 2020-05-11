import os
import pymysql
import time
import scrapy
import json
from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy.settings import Settings
from twisted.internet.defer import inlineCallbacks

from news.spiders.nyt_comments import CommentSpider
from news.items import NewsItem
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings




base = 'http://www.nytimes.com/svc/community/V3/requestHandler?' + 'url=https://www.nytimes.com/2020/04/19/us/coronavirus-moving-city-future.html&sort=oldest&cmd=GetCommentsAll&limit=200&commentSequence='

dbInfo = {
    'host' : 'localhost',
    'port' : 3306,
    'user' : 'root',
    'password' : 'zhao',
    'db' : 'test'
}


conn = pymysql.connect(
                host=dbInfo["host"],
                port=dbInfo["port"],
                user=dbInfo["user"],
                password=dbInfo["password"],
                db=dbInfo['db'],

            )

cursor = conn.cursor()
cursor.execute("use test")
cursor.execute(
    "CREATE TABLE IF NOT EXISTS `comments` (`id` int NOT NULL auto_increment PRIMARY KEY, `commentId` varchar(20), `comment` TEXT NOT NULL, `sentiment` DECIMAL(5, 4) )")




def run_spider():
    process = CrawlerRunner(get_project_settings())

    try:
        sql = 'select * from comments order by id desc limit 1;'
        cursor.execute(sql)
        last_sequence = cursor.fetchall()[0][1]
    except Exception as e:
        print(e)
        last_sequence = '0'
    url = base + last_sequence
    spider = CommentSpider(url=url)
    return process.crawl(spider, url)


# def schedule_next(null, sleep_time):
#     reactor.callLater(sleep_time, crawl)

# def crawl():
#     d = run_spider()
#     d.addCallback(schedule_next, 2)


if __name__ == "__main__":
    run_spider()
    reactor.run()
