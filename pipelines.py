# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


# File: pipelines.py

import os

class MarkdownPipeline:
    def __init__(self):
        self.markdown_folder = "scraped_articles"
        os.makedirs(self.markdown_folder, exist_ok=True)

    def process_item(self, item, spider):
        # Combine metadata table and article content
        full_markdown = item['metadata_table'] + "\n\n" + item['content'].strip()

        # Create a safe filename based on the title
        filename = f"{self.markdown_folder}/{self._safe_filename(item['title'])}.md"

        # Write the combined markdown content to a single file
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(full_markdown)

        spider.log(f"Saved article with metadata: {filename}")
        return item

    def _safe_filename(self, title):
        # Helper method to clean up the title for a safe filename
        return "".join(c if c.isalnum() else "_" for c in title)[:50]
