import scrapy
from scrapy.spiders import Spider


class BCSpider(Spider):
    """
    Spider to crawl and extract information about members from the BC National Assembly website.

    Attributes:
        name (str): The name of the spider.
        allowed_domains (list): A list of allowed domains for the spider.
        start_urls (list): A list of URLs where the spider will start crawling.
    """
    name = "BC"
    allowed_domains = ["leg.bc.ca"]
    start_urls = [
        "https://www.leg.bc.ca/content-committees/pages/mla-contact-information.aspx"]

    def parse(self, response):
        """
        The default callback used by Scrapy to process downloaded responses.

        This method is called when the spider has downloaded a page.
        It extracts links to individual member pages and follows them.

        Args:
            response (scrapy.http.Response): The response object containing the downloaded page content.
        """
        # Extract links to individual member pages and avoid mail to links in table
        mpp_index_links = response.css(
            'table tbody a:not([href^="mailto"])::attr(href)').getall()
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
        name = response.css('h2::text').get().strip(
        ) if response.css('h2::text').get() else ''
        political_affiliation = response.css(
            'div.col-xs-12.col-sm-9.col-md-9 > div:nth-child(1) > div ::text').getall()[6].strip()
        constituency = response.css(
            'div.col-xs-12.col-sm-9.col-md-9 > div:nth-child(1) > div ::text').getall()[2].strip()
        contact_email = response.css('div.convertToEmail ::text').getall()[1].strip() if len(response.css(
            'div.convertToEmail ::text').getall()) > 1 else response.css('div.convertToEmail ::text').getall()[0].strip()
        # telephone = response.css('div.view-content.col-md ::text').getall()[8].strip()
        telephone = ''

        yield {
            'Name': name,
            'Govt': 'Provincial Leader',
            'PoliticalAffiliation': political_affiliation,
            'Constituency': constituency,
            'ProvinceTerritory': 'BC',
            'PreferredLanguage': 'English',
            'Contact': contact_email,
            'Telephone': telephone,
            'Url': response.url
        }
