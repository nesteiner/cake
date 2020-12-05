import scrapy
from cake.items import Album

class Spider(scrapy.Spider):
    name = 'album'
    # start_urls = ['https://www.nvshens.org/girl/21339/album/']
    def __init__(self, db_name=None, links=None, *args, **kwargs):
        self.start_urls = [links]
        self.db_name = db_name
    # ATTENTION remember to modify pipeline
    def parse(self, response):
        album_urls = map(lambda x: response.urljoin(x), response.css('div.igalleryli_title > a.caption::attr(href)').extract())
        # STUB here
        names = response.css('div.igalleryli_title > a.caption::text').extract()
        
        for url, name in zip(album_urls, names):
            yield scrapy.Request(url = url, meta = {'start_link': url, 'name': name, 'album': {'name': name}}, callback = self.take_album)

        # for negativation of albums
        indexs = map(lambda x: x == '下一页', response.css('div.pagesYY a::text').extract())

        if any(indexs):
            next_urls = response.css('div.pagesYY a::attr(href)').extract()
            next_url = response.urljoin(next_urls[-1])
            yield scrapy.Request(url = next_url, callback = self.parse)



    def take_album(self, response):
        # Description return an album
        # single page
        urls = response.css('img::attr(src)').extract()
        names = response.css('img::attr(alt)').extract()
        # put them into response meta
        for url, filename in zip(urls, names):
            response.meta['album'][filename] = url
            
        next_url = response.css('a.a1::attr(href)').extract()[1]
        if next_url.endswith('html'):
            yield scrapy.Request(url = response.urljoin(next_url), callback = self.take_album, meta = {'album': response.meta['album'] })
        else:
            yield response.meta['album']

    

