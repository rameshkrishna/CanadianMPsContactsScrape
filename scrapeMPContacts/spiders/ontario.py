import scrapy
from scrapy.spiders import Spider


class OntarioSpider(Spider):
    """
    Spider to crawl and extract information about members from the Ontario National Assembly website.

    Attributes:
        name (str): The name of the spider.
        allowed_domains (list): A list of allowed domains for the spider.
        start_urls (list): A list of URLs where the spider will start crawling.
    """
    name = "Ontario"
    allowed_domains = ["ola.org"]
    start_urls = ["https://www.ola.org/en/members/parliament-43"]

    def parse(self, response):
        """
        The default callback used by Scrapy to process downloaded responses.

        This method is called when the spider has downloaded a page.
        It extracts links to individual member pages and follows them.

        Args:
            response (scrapy.http.Response): The response object containing the downloaded page content.
        """
        # Extract links to individual member pages
        mpp_index_links = response.css('table tbody a::attr(href)').getall()
        for link in mpp_index_links:
            # Follow each link to the member's detail page
            yield response.follow(link, self.parse_contact)

    def parse_contact(self, response):
        """
        Parses individual member pages to extract detailed contact information about each member.

        Args:
            response (scrapy.http.Response): The response object containing the downloaded page content.

        Yields:
            dict: A dictionary containing extracted information about the member.
        """
        name = response.css(
            'h2.field-content::text').get().strip() if response.css('h2.field-content::text') else ''
        political_affiliation = response.css(
            'div.enteteFicheDepute ul > li:nth-child(2)::text').get()
        constituency = response.css('p.riding a::text').getall()[1].strip() if len(
            response.css('p.riding a::text').getall()) > 1 else ''
        contact_email = response.css(
            'span.field-content a[href^="mailto:"]::text').get()
        # telephone = response.css('div.view-content.col-md ::text').getall()[8].strip()
        telephone = ''  # will fix later not working for every page

        yield {
            'Name': name,
            'PoliticalAffiliation': political_affiliation,
            'Constituency': constituency,
            'ProvinceTerritory': 'Ontario',
            'PreferredLanguage': 'English',
            'Contact': contact_email,
            'Telephone': telephone,
            'Url': response.url
        }
