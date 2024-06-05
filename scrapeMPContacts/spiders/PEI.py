import scrapy
from scrapy.spiders import Spider


class PEISpider(Spider):
    """
    Spider to crawl and extract information about members from the PEI National Assembly website.

    Attributes:
        name (str): The name of the spider.
        allowed_domains (list): A list of allowed domains for the spider.
        start_urls (list): A list of URLs where the spider will start crawling.
    """
    name = "PEI"
    allowed_domains = ["assembly.pe.ca"]
    start_urls = ["https://www.assembly.pe.ca/members"]

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
            '#block-assembly-content > div > div > div > div.view-content.row a::attr(href)').getall()
        for link in mpp_index_links:
            # Follow each link to the
            # member's detail page
            yield response.follow(link, self.parse_contact)

    def parse_contact(self, response):
        """
        Parses individual member pages to extract detailed contact information about each member.

        Args:
            response (scrapy.http.Response): The response object containing the downloaded page content.

        Yields:
            dict: A dictionary containing extracted information about the member.
        """
        name = response.css('h1.title ::text').get()
        political_affiliation = response.css(
            'div.views-field.views-field-field-member-pol-affiliation ::text').get()
        constituency = response.css(
            'div.views-field.views-field-field-member-constituency > div::Text').get()
        contact_email = response.css(
            'div.right-sidebar_sidebar.clearfix.text-formatted.field.field--name-field-member-contact-information.field--type-text-long.field--label-hidden.field__item > p > a ::text').get()
        # telephone = response.css('div.view-content.col-md ::text').getall()[8].strip()
        telephone = response.css(
            'div.right-sidebar_sidebar.clearfix.text-formatted.field.field--name-field-member-contact-information.field--type-text-long.field--label-hidden.field__item > p').re_first(r'Phone:\s*([\d-]+)')

        yield {
            'Name': name,
            'Govt': 'Provincial Leader',
            'PoliticalAffiliation': political_affiliation,
            'Constituency': constituency,
            'ProvinceTerritory': 'PEI',
            'PreferredLanguage': 'English',
            'Contact': contact_email,
            'Telephone': telephone,
            'Url': response.url
        }
