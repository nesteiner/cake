import scrapy
from cake.items import Image

class Spider(scrapy.Spider):
    name = 'cake'
    start_urls = ['https://www.nvshens.org/g/28874/']
    item = Image()                        # global item
    def parse(self,response):
        # all href in a page
        url = response.url
        # yield item: Album
        for image in self.take_images(url, response):
            yield image
        # if next page
        next_url = self.next_url(url, response)
        if next_url != self.start_urls[0]:
            yield scrapy.Request(url=next_url, callback=self.parse)
        # yield Request


    def take_images(self, url, response):
        urls = response.css('img::attr(src)').extract()
        names = response.css('img::attr(alt)').extract()
        for url, name in zip(urls, names):
            self.item['url'] = url
            self.item['name'] = name
            yield self.item
    def next_url(self, url, response):
        href = response.css('a.a1::attr(href)').extract()[1]
        return response.urljoin(href)


