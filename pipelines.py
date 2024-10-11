# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class OtwarteklatkiPipeline:
    def process_item(self, item, spider):
        return item

class MarkdownPipeline:
    def open_spider(self, spider):
        # Open the markdown file in write mode
        self.file = open(f'{spider.name}.md', 'w')
