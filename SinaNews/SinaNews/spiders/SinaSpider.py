# -*- coding: utf-8 -*-

import os
import sys
import scrapy

import re
import logging
from urllib.parse import urlencode
from scrapy.spiders import Rule
from scrapy.cmdline import execute
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request

from fake_useragent import UserAgent
from SinaNews.items import ArticleItem
from SinaNews.spiders.similarity_calculation.similarity import SimilarityCalculation

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
print((os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.dirname(os.path.abspath("E:\PythonFile\SinaNews\SinaNews")))  # 改为项目的绝对路径


class SinaspiderSpider(scrapy.spiders.CrawlSpider):
    name = 'SinaSpider'

    ua = UserAgent()
    start_urls = ['https://search.sina.com.cn/?q=弗洛伊德&c=news&from=&col=&range=all' \
                  '&source=&country=&size=10&stime=&etime=&time=&dpc=0&a=&ps=0&pf=0&page=1']

    Referenced_u = "https://cre.mix.sina.com.cn/api/v3/get?"
    similarity_cal = SimilarityCalculation()

    # 提取搜索结果的下一页链接，调用并使用parse_link。同时提取每一篇新闻链接，调用parse_article
    rules = {  # 如果不指定callback，则默认使用parse_start_url；此外，不能覆盖parse函数
        Rule(LinkExtractor(restrict_xpaths="//div//a[@title='下一页']"),  follow=True),
        Rule(LinkExtractor(restrict_xpaths="//div[@class='box-result clearfix']//h2/a"), callback='parse_article')
        # 这里不需要follow（疑问，如果follow会不会使用第一个Rule）
    }

    def check_stop(self, response):
        self.log(f"跟踪链接：{response.url}", level=logging.INFO)
        article_links = response.xpath("//div[@class='box-result clearfix']//h2/a/@href").extract()

        if not article_links:  # 终止，思考，为什么返回None就终止
            return None

    def parse_article(self, response):
        self.log(f"解析文章内容 + {response.url}", level=logging.INFO)
        # 先返回此新闻的item信息，再返回相关页面的信息
        item = ItemLoader(item=ArticleItem(), response=response)

        item.add_value("Url", response.url)
        title = response.xpath("//h1/text()").extract()
        self.log(title, level=logging.INFO)
        item.add_value("Title", title)
        item.add_xpath("Source", "//div[@class='date-source']/a/text()")
        item.add_xpath("DateTime", "//span[@class='date']/text()")
        Text = "".join(response.xpath("//p//text()").extract()[:-9]).replace(u'\u3000', u' ')

        # 筛选主题相关新闻
        if Text and self.similarity_cal.get_similarity(Text) > 3:
            print(title)
            item.add_value("Text", Text, MapCompose(str.strip))
            yield item.load_item()
            # 相关新闻获取
            params = {
                'cre': 'tianyi',
                'mod': 'pcpager_news',
                'pageurl': response.url,
                'imp_type': '2',
                'this_page': '1'
            }

            r_urls = self.Referenced_u + urlencode(params)
            yield Request(r_urls, callback=self.parse_referenced_url, headers={'User-agent': self.ua.random})
        else:
            self.log(f"没有匹配到正文或主题不相关，url：{response.url}", level=logging.INFO)

    def parse_referenced_url(self, response):
        self.log("[相关新闻的抽取]中-----------------------------------", level=logging.INFO)
        data = response.text
        cmp = re.compile("\"url_https\":\"(https://.*?)\"", )
        links = re.findall(cmp, data)
        for i in links:
            if not re.search('video', i):
                yield Request(i, callback=self.parse_article, headers={"User-Agent": self.ua.random})
            else:
                continue


if __name__ == "__main__":
    execute(['scrapy', 'crawl', 'SinaSpider'])
