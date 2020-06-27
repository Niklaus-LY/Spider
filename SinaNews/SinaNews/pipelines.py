# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# 当parse返回的是item时，调用此文件进行处理


import os
import re
import json
import pandas as pd
# ITEM PIPELINES，管道用于存储和处理ITEM数据


class SinaNewsPipeline:

    count = 0
    # folder = "mini_data"
    # if not os.path.exists(folder):
    #     os.mkdir(folder)
    # data = pd.DataFrame()
    # data_list = []

    def open_spider(self, spider):
        self.index = dict()
        path = "TopicNews"
        if not os.path.exists(path):
            os.mkdir(path)
            print(1)

    def process_item(self, item, spider):
        title = item['Title'][0]
        if not title or self.index.get(title[-10:]):
            return None
        self.index[title[-10:]] = 1
        data = json.dumps(dict(item.items()))
        data = data.encode('utf-8')
        self.count += 1
        with open(f'TopicNews_10_5_2_95_3/{str(self.count)}.json', 'wb') as f:
            f.write(data)
        return item





