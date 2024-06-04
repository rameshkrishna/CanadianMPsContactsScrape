import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider

class OurcommonsSpider(scrapy.Spider):
    """
    A Scrapy spider to crawl and extract information about members from the OurCommons website.

    Attributes:
        name (str): The name of the spider.
        allowed_domains (list): A list of allowed domains for the spider.
        start_urls (list): A list of URLs where the spider will start crawling.
        rules (list): A list of rules for the spider to follow links and parse pages.
    """
    name = "ourcommons"
    allowed_domains = ["ourcommons.ca"]
    start_urls = ["https://www.ourcommons.ca/members/en/search"]
    
    rules = [
        Rule(
            LinkExtractor(
                canonicalize=True,
                unique=True,
                allow_domains=allowed_domains,
            ),
            follow=True,
            callback="parse"
        ),
    ]

    def parse(self, response):
        """
        The default callback used by Scrapy to process downloaded responses.
        
        This method is called when the spider has downloaded a page.
        It extracts links to individual member pages and follows them.

        Args:
            response (scrapy.http.Response): The response object containing the downloaded page content.
        """
        # Extract links to individual member pages
        author_page_links = response.css("a.ce-mip-mp-tile::attr(href)").getall()
        yield from response.follow_all(author_page_links, self.parse_author)

    def parse_author(self, response):
        """
        Parses individual member pages to extract detailed information about each member.

        Args:
            response (scrapy.http.Response): The response object containing the downloaded page content.

        Yields:
            dict: A dictionary containing extracted information about the member.
        """
        yield {
            'Name': response.css('h1::text').get(),
            'Political Affiliation': response.css('dd.mip-mp-profile-caucus::text').get(),
            'Constituency': response.css('dd a::text').get(),
            'Province/Territory': response.css('dt:contains("Province / Territory:") + dd::text').get(),
            'Preferred Language': response.css('dt:contains("Preferred Language:") + dd::text').get(),
            'Contact': response.css('#contact a::text').get(),
            'Telephone': response.css('p:contains("Telephone")::text').re_first(r'Telephone:\s+([\d-]+)'),
            'Url': response.url
        }
