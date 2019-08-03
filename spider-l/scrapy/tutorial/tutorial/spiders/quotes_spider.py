import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        urls = [
                'http://quotes.toscrape.com/',
                ]
        tag = getattr(self, 'tag', None)
        if tag is not None:
            url = url+'tag/'+tag

        yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                    'text': quote.css('span.text::text').get(),
                    'author': quote.css('small.author::text').get(),
                    'tags': quote.css('div.tags a.tag::text').getall(),
                }
        
        # next_page = response.css('li.next a::attr(href)').get()
    
        # if next_page is not None:
            # use scrapy.Request.
            # next_page = response.urljoin(next_page)
            # yield scrapy.Request(next_page, callback=self.parse)
            
            # use the shortcut.
            # response.follow supports relative URLs directly.
            # yield response.follow(next_page, callback=self.parse)

        # you can also use <a> elements directly.
        for a in response.css('li.next a'):
            yield response.follow(a, callback=self.parse)
