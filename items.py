# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

# File: items.py

import scrapy

class ArticleItem(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    author = scrapy.Field()
    publication_date = scrapy.Field()
    content = scrapy.Field()
    metadata_table = scrapy.Field()
