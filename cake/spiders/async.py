import scrapy
from cake.items import Album

class Spider(scrapy.Spider):
    name = 'async'
    start_urls = ['http://pic.netbian.com/4kmeinv/index.html']

    def parse(self, response):
        # TODO get all images and names from one page
        part_urls = response.css('div.slist ul.clearfix li a img::attr(src)').extract()
        urls = map(lambda url: response.urljoin(url), part_urls)
        names = response.css('div.slist ul.clearfix li a img::attr(alt)').extract()
        yield {'urls': urls,
               'names': names}
        # yield item
        
        hasNext = response.css('div.page a::text').extract()[-1] == '下一页'
        if(hasNext):
            nextPageUrl = response.urljoin(response.css('div.page a::attr(href)').extract()[-1])
            yield scrapy.Request(url = nextPageUrl, callback = self.parse)

            
    

