# -*- coding: utf-8 -*-
import os
import re
import sys
import time
import zipfile
import requests

from math import ceil
from queue import Queue
from threading import Thread
from pyquery import PyQuery as pq
from fake_useragent import UserAgent

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class beautifulGUI(QWidget):

    def __init__(self):
        super().__init__()
        self._design()

    def _design(self):

        # 初始化窗口位置，大小
        self.setGeometry(200, 200, 650, 450)

        # 设置窗口标题、图标
        self.setWindowTitle("并购家爬虫")
        self.setWindowIcon(QIcon("images\logo.png"))

        # 设置背景图片
        window_pale = QPalette()
        window_pale.setBrush(self.backgroundRole(), QBrush(QPixmap(r"images\background.jpg")))
        self.setPalette(window_pale)

        # 设置透明度
        self.setWindowOpacity(0.8)

        # 提示标签和关键词输入框
        text1 = QLabel()
        text1.setText("请输入搜索关键词:")
        text1.setFont(QFont("楷体", 17))

        self.name_box = QLineEdit()

        # 对应的横向布局
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(text1, stretch=2)
        hbox.addWidget(self.name_box, stretch=8)
        hbox.addStretch(3)

        # 提示标签和数量输入框
        text2 = QLabel()
        text2.setText("请输入爬取篇数:  ")
        text2.setFont(QFont("楷体", 17))
        self.amount_box = QLineEdit()

        # 对应的横向布局
        hbox2 = QHBoxLayout()
        hbox2.addStretch(1)
        hbox2.addWidget(text2, stretch=2)
        hbox2.addWidget(self.amount_box, stretch=8)
        hbox2.addStretch(3)

        # 爬虫启动按钮（未绑定操作）
        self.startButton = QPushButton()
        self.startButton.setText("开始爬取")
        self.startButton.setFont(QFont("楷体", 15))

        hbox3 = QHBoxLayout()
        hbox3.addStretch(8)
        hbox3.addWidget(self.startButton, stretch=2)
        hbox3.addStretch(2)

        # 状态显示框
        self.statusBrowser = QTextBrowser()
        self.statusBrowser.setText("爬虫未启动！")

        hbox4 = QHBoxLayout()
        hbox4.addStretch(1)
        hbox4.addWidget(self.statusBrowser, stretch=10)
        hbox4.addStretch(2)

        # 用一个竖直布局作为整体布局
        vbox = QVBoxLayout()
        vbox.addStretch(2)
        vbox.addLayout(hbox, stretch=5)
        vbox.addStretch(2)
        vbox.addLayout(hbox2, stretch=5)
        vbox.addStretch(1)
        vbox.addLayout(hbox3)
        vbox.addStretch(2)
        vbox.addLayout(hbox4, stretch=8)
        vbox.addStretch(2)

        # 设置主布局
        self.setLayout(vbox)



class mySpider(beautifulGUI):

    def __init__(self):

        # 界面部分
        super().__init__()
        self.startButton.clicked.connect(self._start)
        self.show()

        # 计时部分
        self.stime, self.etime = None, None

        # 爬虫部分
        self.name = None
        self.amount = None
        self.count = 0

        self.url = ""
        self.thread_queue = Queue()
        self.url_list = []
        self.cookie = None
        self.ua = UserAgent()
        # 初始请求头
        self.headers_url = {
            'user-agent': self.ua.random,
        }

        # 下载时的请求头
        self.headers_download = {
            "User-Agent": self.ua.random,
            'If-None-Match': "76cca25ec3ddd51:0",
            'Cookie': '',
            'Referer': '',
        }


    def _start(self):
        # 控件功能由子线程负责
        Thread(target=self._action).start()

    def _action(self):
        try:
            self.stime = time.time()
            name, amount = self.name_box.text(), self.amount_box.text()
            if not amount.isdigit():
                self.statusBrowser.append("输入有误！请输入正确的篇数。")  # 不能使用setText
                self.amount_box.clear()
            amount = int(amount)
            self.statusBrowser.append(f"\n\n关键词：{name},  数量：{amount}")
            self.statusBrowser.append("爬虫启动".center(30, "*"))
            self.name, self.amount = name, amount
            self.count = 0
            self.url = f'http://www.ipoipo.cn/search.php?q={self.name}'
            html = self._getResponse()

            if not html:
                self.statusBrowser.append("请求出现异常，程序终止。")
                # QApplication.processEvents()

                return None

            # 检测搜索是否有结果，并且搜索结果的总页数
            flag, total_page = self._check_and_getPage(html)

            if not flag:
                self.statusBrowser.append("搜索无果！")
                # QApplication.processEvents()
                self.name_box.clear()
                self.amount_box.clear()

                return None

            # amount篇报告占搜索结果的页数，每页最多有21篇报告
            need_page = ceil(self.amount / 21)

            # 取较小者为需要最后爬取的页数。
            # 两种情况： 供大于求————节省时间； 供小于求————避免爬到空白页面
            page = min(total_page, need_page)

            # 获取全部的报告链接
            self._getAllReportUrl(page)

            # 下载报告
            self._Download()

        except Exception as e:
            print(e)
            exit(0)

    def _getResponse(self):
        try:
            response = requests.get(self.url, headers=self.headers_url)
            response.raise_for_status()  # 状态码不是200，则抛出HTTPError异常
            response.encoding = 'utf-8'
            if not self.cookie:
                # 保留会话的cookie
                d_cookie = requests.utils.dict_from_cookiejar(response.cookies)
                Cookie = "".join([f"{key}={value}; " for key, value in d_cookie.items()])
                self.cookie = Cookie

            return response.text

        except requests.exceptions.ConnectTimeout:
            self.statusBrowser.append("链接超时！")
            # QApplication.processEvents()

            return  None
        except requests.exceptions.ConnectionError:
            self.statusBrowser.append("连接出错！")
            # QApplication.processEvents()

            return None

    def _check_and_getPage(self, html):
        '''
          检查搜索结果，并且进行解析, 有三种情况
        1. 搜索无果，找不到相关报告
        2. 存在搜索结果，但只有一页
        3. 存在搜索结果，至少有两页

        :param html: 网页代码
        :return: 搜索结果是否存在，总页码数
        '''

        items = list(pq(html)('.multi-ellipsis a').items())
        if len(items) == 0:

            return False, None

        comp = re.compile("page=(\d*)\" title=\"最后一页\"")
        last_page = re.findall(comp, html)

        pages = 1
        if last_page != []:
            pages = int(last_page[0])

        self.statusBrowser.append(f"搜索结果共有{str(pages)}页，每页最大篇数为21.")
        # QApplication.processEvents()

        return True, pages


    def _getAllReportUrl(self, page):

        for p in range(1, page + 1):
            self.url = f'http://www.ipoipo.cn/search.php?q={self.name}&page={str(p)}'
            html = self._getResponse()
            urls = self._parse_reportUrl(html)
            self.url_list.extend(urls)
            if len(self.url_list) >= self.amount:
                return

    def _parse_reportUrl(self, html):
        """
        从网页中解析出报告的链接地址
        """

        urls = []
        items = list(pq(html)('.multi-ellipsis a').items())
        for i in items:
            r = i.attr('href')
            urls.append(r)

        return urls

    def _Download(self):
        """
        观察发现，报告url修改post字段为download即可跳转到下载链网页，注意保留post的链接作为Referer属性的值（防盗链）
        """

        # 创建文件夹
        if not os.path.exists("reports"):
            os.mkdir('reports')

        file_folder = 'reports' + os.sep + self.name
        if not os.path.exists(file_folder):
            os.mkdir(file_folder)
        os.chdir(file_folder)

        for u in self.url_list:
            self.headers_download['Referer'] = u  # 网页设置了防盗链，需要记录上一次进入的页面地址
            self.url = u.replace("post", "download")  # 修改字段即可，没必要再访问一次

            html = self._getResponse()
            compile = re.compile('http://(?:www.)?ipoipo.cn/zb_users/upload/(.*?).zip') # 高级正则表达式用法，只匹配不获取
            match_succesful = re.findall(compile, html)

            if  match_succesful:
                result = match_succesful[0]
                link = f"http://www.ipoipo.cn/zb_users/upload/{result}.zip"
                dl_thread = Thread(target=self._download, args=(link, os.getcwd(), self.count + 1))
                dl_thread.start()
                self.thread_queue.put(dl_thread)
                self.statusBrowser.append(f"第{self.count + 1}篇开始爬取！")
                self.count = self.count + 1
                if self.count == self.amount:
                    break

        self._clear()


    def _clear(self):

        self._wait()  # 主进程等待所有子进程结束
        self.etime = time.time()
        cost = self.etime - self.stime
        self.statusBrowser.append(f"已爬取所有搜索结果，任务结束。任务用时{cost:.2f}秒。\n\n")

        # 清空输入框
        self.name_box.clear()
        self.amount_box.clear()
        os.chdir('../..')  # 回到上上级目录，即report的上级目录


    def _wait(self):
        '''
        等待所有子线程结束后，主线程才结束
        '''

        while not self.thread_queue.empty():
            self.thread_queue.get().join()

    def _download(self, link, path, count):
        """
        下载报告并解压到一个文件夹
        :param link:
        :return:
        """

        self.headers_download['Cookie'] = self.cookie
        response = requests.get(link, headers=self.headers_download)

        # 数据写入文件
        fileName = path + os.sep + f'{str(count + 1)}.zip'
        with open(fileName, 'wb')as f:
            f.write(response.content)

        # 解压并删除压缩包，首先改文件名的编码
        extracting = zipfile.ZipFile(fileName)
        oldFile = extracting.filelist[0].filename  # 火星文
        newFile = extracting.filelist[0].filename.encode('cp437').decode("gbk")  # 人类可读文件名
        extracting.extractall()  # 解压文件
        extracting.close()  # 关闭压缩文件
        os.remove(fileName)  # 删除压缩文件
        os.rename(oldFile, newFile) # 解压后的文件重命名

        self.statusBrowser.append(f"第{count}篇爬取完毕！")
        # QApplication.processEvents()



if __name__ == '__main__':

    app = QApplication(sys.argv)
    print("程序启动。")
    spider = mySpider()
    sys.exit(app.exec_())
