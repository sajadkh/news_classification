import scrapy


class NewsSpider(scrapy.Spider):
    name = 'news'

    start_urls = [
		 'http://www.tehrantimes.com/service/society',
                 'http://www.tehrantimes.com/service/sports',
		 'http://www.tehrantimes.com/service/politics',
                 'http://www.tehrantimes.com/service/economy',
                 ]

    def parse(self, response):
        # follow links to author pages
        for href in response.css('li.news a::attr(href)'):
            yield response.follow(href, self.parse_news)

        # follow pagination links
        for href in response.css('.box a::attr(href)'):
            yield response.follow(href, self.parse)

    def parse_news(self, response):
        yield {
            'subject': response.xpath("//ol[@class='breadcrumb']/li/a/text()").extract(),
            'headline': response.xpath("//h2[@class='item-title']/text()").extract(),
            'date': response.xpath("//div[@class='item-date half-left']/text()").extract(),
	    'text': response.xpath("//div[@class='item-text']/p/text()").extract(),
        }

