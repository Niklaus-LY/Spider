# -*- coding: utf-8 -*-
# @Time    : 2020/6/24 0024 12:33
# @Author  : Niklaus
# @File    : result_graph.py
# @Software: PyCharm

from matplotlib import pyplot as plt

with open('标注1051932.3.txt', 'r') as f:
    label = []
    t = f.readlines()
    for i in t:
        label.append(i.strip())
    print(label)
    print(len(label))
    l = len(label)
    count = [label[:i].count('1') / (i+1)  for i in range(len(label))]
    print(count)
    plt.plot(range(1, 251), count)
    plt.title("10_5_1_93_2.3", fontsize=16)
    plt.show()


with open('标注1052953.txt', 'r') as f:
    label = []
    t = f.readlines()
    for i in t:
        label.append(i.strip())
    print(label)
    print(len(label))
    l = len(label)
    count = [label[:i].count('1') / (i+1)  for i in range(len(label))]
    print(count)
    plt.plot(range(1, 251), count)
    plt.title("10_5_2_95_3", fontsize=16)
    plt.show()
