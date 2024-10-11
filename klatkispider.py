import scrapy

class klatkispiderSpider(scrapy.Spider):
    name = 'klatkispider'
    allowed_domains = ['otwarteklatki.pl']
    start_urls = ['https://www.otwarteklatki.pl/blog']

    def parse(self, response):
        # Select each article block
        articles = response.xpath('//div[@class="blog-tile"]')

        for article in articles:
            # Extract the link, title, date, and description from each article
            yield {
                'title': article.xpath('.//div[@class="post"]//div[@class="info"]//h3//text()').get(),
                'date': article.xpath('.//div[@class="post"]//div[starts-with(@class,"date")]//span/span//text()').get(),
                'description': article.xpath('.//div[@class="post"]//div[@class="info"]//p[contains(@class,"preview")]').get(),
            }

        # Follow the pagination links (if there are more pages)
        next_page = response.xpath('(//div[starts-with(@class,"pagination")]//div/a/@href)[1]').get()
        if next_page:
            yield response.follow(next_page, self.parse)
