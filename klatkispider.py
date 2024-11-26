import scrapy
import os

class KlatkiSpider(scrapy.Spider):
    name = "klatkispider"
    allowed_domains = ["otwarteklatki.pl"]
    start_urls = ["https://www.otwarteklatki.pl/blog"]

    # Set a folder to save markdown files
    markdown_folder = "scraped_articles"

    # Create the folder if it doesn't exist
    os.makedirs(markdown_folder, exist_ok=True)

    def parse(self, response):
        # Extract all article links using XPath
        article_links = response.xpath('//div[@class="blog-tile"]//a/@href').getall()

        # Follow each article link to scrape the content
        for link in article_links:
            yield response.follow(link, self.parse_article)

        # Pagination - find next page link and follow it if exists
        next_page = response.xpath('(//div[@class="flex center-xs fs-h3"]/a/@href)[1]').get()
        if next_page:
            yield response.follow(next_page, self.parse)

    def parse_article(self, response):
        # Extract article title, author, publication date, subheadings and content paragraphs
        title = response.xpath('//h1/text()').get().strip()
        author = response.xpath('//div[starts-with(@class,"post-info")]/a/text()').get()
        publication_date = response.xpath('//div[starts-with(@class,"post-info")]/span/text()').get()
        subheadings = response.xpath('//div[contains(@class, "post-content")]//strong/text()').getall()
        content_paragraphs = response.xpath('//div[contains(@class, "post-content")]//p/text()').getall()

        # Ensure all fields are non-empty
        author = author if author else "N/A"
        publication_date = publication_date if publication_date else "N/A"

        # Build the metadata section as a table
        metadata_table = "| Title              | URL                | Author             | Publication Date   |\n"
        metadata_table += "|--------------------|--------------------|--------------------|--------------------|\n"
        metadata_table += f"| {title} | {response.url} | {author} | {publication_date} |\n"

        # Build the article content section in Markdown
        article_markdown = f"# {title}\n\n"
        for i, paragraph in enumerate(content_paragraphs):
            article_markdown += f"{paragraph.strip()}\n\n"
            if i < len(subheadings):
                article_markdown += f"**{subheadings[i].strip()}**\n\n"

        # Combine metadata table and article content
        full_markdown = metadata_table + "\n\n" + article_markdown

        # Create a safe filename based on the title
        filename = f"{self.markdown_folder}/{self._safe_filename(title)}.md"

        # Write the combined markdown content to a single file
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(full_markdown)

        self.log(f"Saved article with metadata: {filename}")

    def _safe_filename(self, title):
        # Helper method to clean up the title for a safe filename
        return "".join(c if c.isalnum() else "_" for c in title)[:50]
