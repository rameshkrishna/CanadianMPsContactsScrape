import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider

class QuebecSpider(CrawlSpider):
    """
    A Scrapy spider to crawl and extract information about members from the Quebec National Assembly website.

    Attributes:
        name (str): The name of the spider.
        allowed_domains (list): A list of allowed domains for the spider.
        start_urls (list): A list of URLs where the spider will start crawling.
        rules (list): A list of rules for the spider to follow links and parse pages.
    """
    name = "Quebec"
    allowed_domains = ["assnat.qc.ca"]
    start_urls = ["https://www.assnat.qc.ca/en/deputes/index.html"]

    rules = [
        Rule(
            LinkExtractor(
                canonicalize=True,
                unique=True,
                allow_domains=allowed_domains,
                allow=['/en/deputes/'],
                deny=['/fr/deputes/']
            ),
            follow=False,
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
        # Extract links from the table with ID `ListeDeputes`
        mpp_index_links = response.css("#ListeDeputes a:not(.nePasRediriger)::attr(href)").getall()
        for link in mpp_index_links:
            if '/en/deputes/' in link:
                link = link.replace('index.html', 'coordonnees.html')
                yield response.follow(link, self.parse_contact)

    def parse_contact(self, response):
        """
        Parses individual member pages to extract detailed contact information about each member.

        Args:
            response (scrapy.http.Response): The response object containing the downloaded page content.

        Yields:
            dict: A dictionary containing extracted information about the member.
        """
        print(response.url)
        yield {
            'Name': ' '.join(response.css("h1 ::text").getall()),
            'PoliticalAffiliation': response.css('div.enteteFicheDepute ul > li:nth-child(2)::text').get(),
            'Constituency': response.css('div.enteteFicheDepute > ul > li:nth-child(1) ::text').get(),
            'ProvinceTerritory': 'Quebec',
            'PreferredLanguage': 'French',
            'Contact': response.css('div.blockAdresseDepute a[href^="mailto:"]::attr(href)').get(),
            'Telephone': response.css('div.blockAdresseDepute span.paragraph').re_first(r'Telephone:\s*([\d-]+)'),
            'Url': response.url
        }
