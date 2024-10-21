import scrapy
import os

class klatkispiderSpider(scrapy.Spider):
    name = "klatkispider"
    allowed_domains = ["otwarteklatki.pl"]
    start_urls = ["https://www.otwarteklatki.pl/blog"]

    # Set folder to save markdown files
    markdown_folder = "scraped_articles"

    # Create the folder if it doesn't exist
    if not os.path.exists(markdown_folder):
        os.makedirs(markdown_folder)

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
        # Extract article title
        title = response.xpath('//h1/text()').get().strip()

        # Extract subheadings, content
        subheadings = response.xpath('//article/p//strong').getall()
        content_paragraphs = response.xpath('//div[contains(@class, "post-content")]//p/text()').getall()

        # Combine content paragraphs
        content = "\n\n".join(content_paragraphs).strip()

        # Bold the subheadings
        formatted_subheadings = [f"**{subheading.strip()}**" for subheading in subheadings]

        # Insert subheadings into the content (for demonstration, after each paragraph)
        markdown_content = f"# {title}\n\n"
        for i, paragraph in enumerate(content_paragraphs):
            markdown_content += f"{paragraph.strip()}\n\n"
            if i < len(formatted_subheadings):
                markdown_content += f"{formatted_subheadings[i]}\n\n"

        # Generate a markdown string
        markdown_content = f"# {title}\n\n{content}"

        # Create a safe filename based on the title
        filename = f"{self.markdown_folder}/{self._safe_filename(title)}.md"

        # Write the markdown content to a file
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(markdown_content)

    def _safe_filename(self, title):
        # Helper method to clean up the title for a safe filename
        return "".join(c if c.isalnum() else "_" for c in title)[:50]
