## cake 爬虫
闲着没事，写了个爬虫去怕去宅男女神的爬虫，以前写的介绍在`docs/info.md`里
两个多月没碰了，打算重写这个项目
## 运行代码
### 软件需要
- `scrapy`
- `python3`
- `mongodb`
### 配置需要
在`setting.py`中开启`PIPELINE`
```python3
ITEM_PIPELINES = {
  'cake.pipelines.CakePipeline': 300,
}
```

### 使用方法
#### 1. 爬取链接
`scrapy crawl album -a db_name="the db where you use " -a links="the start of album page"`
**注意**
你只是存储了这些图片的链接，而不是文件 
另外在下载这些图片时很容易被网站303，现在还没解决

#### 2. 下载图片
TODO 
### 代码结构
爬虫模块 
`cake`
下载模块
`downloader`
### 待办事项
- [ ] `downloader`
