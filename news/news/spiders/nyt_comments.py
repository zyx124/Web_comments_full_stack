import scrapy
from ..items import NewsItem
import pymysql
import json
import csv
import os



FILE_PATH = str(os.getcwd())

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

name = "comment_spider"
allowed_domains = ["nytimes.com"]
base = 'http://www.nytimes.com/svc/community/V3/requestHandler?' + 'url=https://www.nytimes.com/2020/04/19/us/coronavirus-moving-city-future.html&sort=oldest&cmd=GetCommentsAll&limit=200&commentSequence='
start_urls = [base]


class CommentSpider(scrapy.Spider):
    name = 'comment_spider'
    def __init__(self, url, *args, **kwargs):
        super().__init__()
        self.start_urls = [url]

    def start_requests(self):
        try:
            yield scrapy.Request(url=self.start_urls[0], callback=self.parse)
        except Exception as e:
            print(e)

    def parse(self, response):
        content = json.loads(response.text)
        comments = content['results']['comments']
        for c in comments:
            item = NewsItem()
            item['commentID'] = str(c['commentID'])
            item['comment'] = str(c['commentBody'])
            yield item
