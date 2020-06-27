# -*- coding: utf-8 -*-

# Scrapy settings for SinaNews project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'SinaNews'

SPIDER_MODULES = ['SinaNews.spiders']
NEWSPIDER_MODULE = 'SinaNews.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'SinaNews (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'SinaNews.middlewares.SinanewsSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    'SinaNews.middlewares.SinanewsDownloaderMiddleware': 543,
# }

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'SinaNews.pipelines.SinaNewsPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'


# 配置请求头
from fake_useragent import UserAgent
# HTTPERROR_ALLOWED_CODES = [404]
# USER_AGENT = 'quotesbot (+http://www.yourdomain.com)'
# USER_AGENT = UserAgent().random

# 配置编码参数
FEED_EXPORT_ENCODING = 'utf-8'

# 配置日志级别
from datetime import datetime

# 文件及路径，log目录需要先建好
import os
if not os.path.exists('logging'):
   os.mkdir('logging')

today = datetime.now()
LOG_FILE_PATH = "logging/scrapy_{}_{}_{}_{}_{}.log".format(today.year, today.month, today.day, today.hour, today.minute)
LOG_FORMAT = '%(asctime)s [%(name)s] %(levelname)s: %(message)s'

# 日志输出
LOG_LEVEL = 'INFO'
LOG_FILE = LOG_FILE_PATH

# 设置爬虫停止条件，等于0代表不开启
# CLOSESPIDER_TIMEOUT = 10  # 限定时间
CLOSESPIDER_ITEMCOUNT = 250  # 限定Item数目，存在不准确的情况
# CLOSESPIDER_PAGECOUNT = 10  # 限定抓取的页面数
# CLOSESPIDER_ERRORCOUNT = 10  # 限定出错数量

# HTTP缓存和离线运行——第二次运行的时候可以快速得到部分结果
# HTTPCACHE_ENABLE = True
# THHPCAHCE_POLICY = scrapy.contrib.httpcache.RFC2616Policy


# 重试策略
RETRY_ENABLE = True
RETRY_TIMES = 5
# RETRY_HTTP_CODES = 400 # 移除重试的错误码

# 延迟
DOWNLOAD_DELAY = 2

# 设置并发数
CONCURRENT_REQUESTS = 32

# 爬虫的恢复
# JOB_DIR = "JOB"

# 广度优先
DEPTH_PRIORITY = 1
SCHEDULER_DISK_QUEUE = 'scrapy.squeues.PickleFifoDiskQueue'
SCHEDULER_MEMORY_QUEUE = 'scrapy.squeues.FifoMemoryQueue'
