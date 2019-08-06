import scrapy
import time

class QsbkSpider(scrapy.Spider):
    name = "qsbk"
    # 注意，在这里是start_urls，而不是urls
    # 需要在设置文件中修改请求头，否则服务器不响应
    start_urls = ['https://www.qiushibaike.com/text/',]


    def parse(self, response):
        content_blocks = response.xpath("//div[@id='content-left']/div")

        # for content_block in content_blocks:
        #     author = content_block.xpath(".//h2/text()").get().strip()
        #     content = content_block.xpath(".//div[@class='content']//text()").getall()
        #     content = "".join(content).strip()

        #     yield {"author":author, "content": content}

        for content_block in content_blocks:

            href = content_block.xpath(".//a[@class='contentHerf']/@href").get()
            time.sleep(0.2) # 程序跑太快访问会被拒绝
            yield response.follow(href, self.content_parse)

        # 点击下一页, 如果找不到则返回None
        next_page = response.xpath("//ul[@class='pagination']/li/a/span[@class='next']/../@href").get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

    def content_parse(self, response):

        author = response.xpath("//span[@class='side-user-name']/text()").get()
        like = response.xpath("//i[@class='number']/text()").get()

        # 必须是getall()， 否则只能显示第一行
        content = response.xpath("//div[@class='content']/text()").getall()
        content = ''.join(content)

        yield {
                "author" : author,
                "like" : like,
                "url" : response.url,
                "content" : content,
                }