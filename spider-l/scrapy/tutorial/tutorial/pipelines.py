# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# # export a list
# from scrapy.exporters import JsonItemExporter

# class QsbkPipeline(object):

#     def open_spider(self, spider):
#         self.fp = open("qsbk.json", "wb")# , encoding="utf-8")
#         self.exporter = JsonItemExporter(self.fp, ensure_ascii=False)
#                                         # encoding='utf-8')
        # self.exporter.start_exporting()

#     def process_item(self, item, spider):
#         self.exporter.export_item(item)
#         return item

#     def close_spider(self, spider):
#         self.exporter.finish_exporting()
#         self.fp.close()


from scrapy.exporters import JsonLinesItemExporter

class QsbkPipeline(object):

    def open_spider(self, spider):
        self.fp = open("qsbk.jl", "wb")# , encoding="utf-8")
        self.exporter = JsonLinesItemExporter(self.fp, ensure_ascii=False,
                                        encoding='utf-8')

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.fp.close()