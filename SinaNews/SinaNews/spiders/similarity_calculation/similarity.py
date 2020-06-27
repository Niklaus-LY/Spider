# -*- coding: utf-8 -*-
# @Time    : 2020/6/22 0022 19:05
# @Author  : Niklaus
# @File    : similarity.py
# @Software: PyCharm

# 750篇新闻计算相似度
# 排序，画图，选定阈值
# 找不到也没关系，定的越高，主题越集中

import json
from jieba import analyse
from pyhanlp import *
from matplotlib import pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False


class SimilarityCalculation:

    def __init__(self):
        self.topic = ["弗洛伊德", "佛洛伊德", "乔治·弗洛伊德"]
        self.topic_word = ['跪', '黑人', '白人', '警察', '抗议', '暴乱', '美国', '示威', '种族歧视', "枪击", "抢劫", "镇压"]
        self.CSD = JClass('com.hankcs.hanlp.dictionary.CoreSynonymDictionary')

    def get_similarity(self, document):
        if not document:
            return 0

        keys = analyse.extract_tags(document)  # 抽取关键词
        len_keys = len(keys)
        topic_count = 1
        if self.topic[0] in keys or self.topic[1] in keys or self.topic[2] in keys:  # 主题词更重要
            topic_count += 5
        for w in self.topic_word:
            for k in keys:
                if k == w:
                    topic_count += 3
                elif self.CSD.similarity(w, k) > 0.91:
                    topic_count += 1
        return topic_count / len_keys


if __name__ == '__main__':

    result = []
    for i in range(1, 750):
        with open(rf"sample/file{str(i)}.json", 'rb') as f:
            document = json.load(f)['Text'][0]
            # print(document)
            sc = SimilarityCalculation()
            sim = sc.get_similarity(document)
            # print(sim)
            result.append(sim)

    result_ranking = list(sorted(result))
    print(result_ranking)
    print(len(result_ranking))

    plt.scatter(range(1, len(result_ranking) + 1), result_ranking, s=0.5)
    plt.title("主题相关度结果", fontsize=20)
    plt.xlabel("新闻数量", fontsize=16)
    plt.ylabel("主题相关度", fontsize=16)
    plt.show()

    # 饼图
    y = []
    n = 1
    start = 0.5
    count = 0
    for i in result_ranking:
        if i <= start * n:
             count += 1
        else:
            y.append(count)
            count = 0
            n += 1

    labels = ['0-0.5', '0.5-1', '1-1.5', '1.5-2', '2-2.5', '2.5-3']

    # 每一部分的突出程度
    explode = (0, 0, 0, 0, 0, 0.1)
    # autopct表示显示百分数的形式，shadow是否有阴影效果，startangle是起始角度
    plt.pie(y, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=False, startangle=90)
    # 将饼图变为正圆
    plt.axis('equal')
    plt.title("各区间比例")
    plt.show()

    # 1.5的时候有较大的区分，但为了更精确，选择2。
    # 90 篇中83篇相关新闻










