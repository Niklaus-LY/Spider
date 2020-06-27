### 主题爬虫
----  
#### 对象
新浪新闻

#### 搜索模式
- 搜索界面——>搜索结果所有新闻——>每篇新闻下面的相关新闻——>

#### 问题
- 存在某些新闻链接一样 * ——在下载中间件做去重处理
- 存在链接不一样的两篇新闻，但内容大同小异 **** ——在Item Pipeline中对标题做去重处理，可以考虑数据库表的URL和title同时作为index
- 存在网页格式不一致 ***** 链接直接抽取
- 有时候不是广度优先？******爬取速度过快 
   1. 100  120
   2. 广
     
     
- 同一个文件的日志怎么分隔

#### 录制视频的策略
— 停止设置跟爬取的不符合 ***因为是并发执行的，满足停止条件的时候部分请求队列里面有存在活动的线程
- 深度优先和广度优先
  - 并发数设置为1，每次运行后删除Files文件夹，因为已经部分爬取过的不会再爬取(爬虫缓存)
  - 设置爬取策略和递归深度（策略为1为广度优先，策略=0时为深度优先，爬取深度可以设置）