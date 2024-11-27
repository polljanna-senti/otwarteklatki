# File: spiders/klatki_spider.py

import scrapy
from ..items import ArticleItem

class KlatkiSpider(scrapy.Spider):
    name = "klatkispider"
    allowed_domains = ["otwarteklatki.pl"]
    start_urls = ["https://www.otwarteklatki.pl/blog"]

    def parse(self, response):
        # Extract all article links using XPath
        article_links = response.xpath('//div[@class="blog-tile"]//a/@href').getall()

        # Follow each article link to scrape the content
        for link in article_links:
            yield response.follow(link, self.parse_article)

        # Pagination - find the next page link and follow it if it exists
        next_page = response.xpath('(//div[@class="flex center-xs fs-h3"]/a/@href)[1]').get()
        if next_page:
            yield response.follow(next_page, self.parse)

    def parse_article(self, response):
        # Extract article data
        title = response.xpath('//h1/text()').get().strip()
        author = response.xpath('//div[starts-with(@class,"post-info")]/a/text()').get() or "N/A"
        publication_date = response.xpath('//div[starts-with(@class,"post-info")]/span/text()').get() or "N/A"

        # Build metadata table
        metadata_table = "| Title              | URL                | Author             | Publication Date   |\n"
        metadata_table += "|--------------------|--------------------|--------------------|--------------------|\n"
        metadata_table += f"| {title} | {response.url} | {author} | {publication_date} |\n"

        # Build article content
        content_nodes = response.xpath('//div[contains(@class, "post-content")]/*')
        content = ""
        for node in content_nodes:
            if node.root.tag == 'strong':
                bold_text = node.xpath('text()').get().strip()
                content += f"**{bold_text}** "  # Add inline bold text
            else:
                paragraph_text = node.xpath('string(.)').get()
                if paragraph_text:
                    content += f"{paragraph_text.strip()}\n\n"

        # Create an ArticleItem for the pipeline
        item = ArticleItem()
        item['title'] = title
        item['url'] = response.url
        item['author'] = author
        item['publication_date'] = publication_date
        item['metadata_table'] = metadata_table
        item['content'] = content

        yield item

