import scrapy


class QsbkSpider(scrapy.Spider):
    name = "qsbk"
    # 注意，在这里是start_urls，而不是urls
    start_urls = ['https://www.qiushibaike.com/text/',]


    def parse(self, response):
        print('Hello, world')
        content_blocks = response.xpath("//div[@id='content-left']/div")

        for content_block in content_blocks:
            author = content_block.xpath(".//h2/text()").get().strip()
            content = content_block.xpath(".//div[@class='content']//text()").getall()
            content = "".join(content).strip()

            yield {"author":author, "content": content}