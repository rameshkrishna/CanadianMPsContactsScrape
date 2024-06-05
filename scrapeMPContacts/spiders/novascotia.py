import scrapy
from scrapy.spiders import Spider


class NovaSpider(Spider):
    """
    Spider to crawl and extract information about members from the Nova National Assembly website.

    Attributes:
        name (str): The name of the spider.
        allowed_domains (list): A list of allowed domains for the spider.
        start_urls (list): A list of URLs where the spider will start crawling.
    """
    name = "Nova"
    allowed_domains = ["nslegislature.ca"]
    start_urls = ["https://nslegislature.ca/members/profiles-table"]

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
        name = response.css('h1 ::text').get().strip(
        ) if response.css('h1 ::text').get() else ''
        political_affiliation = response.css(
            'table > tbody > tr > td.views-field.views-field-field-party ::text').get().strip()
        constituency = response.css(
            'table > tbody > tr > td.views-field.views-field-field-constituency ::text').get().strip()
        contact_email = response.css(
            'div.panel-pane.pane-dsc.mla-current-profile-contact a ::text').get()

        telephone = response.css(
            'div.panel-pane.pane-dsc.mla-current-profile-contact p:contains("Phone:")').re_first(r'Phone:\s*([\d-]+)')

        yield {
            'Name': name,
            'PoliticalAffiliation': political_affiliation,
            'Constituency': constituency,
            'ProvinceTerritory': 'Nova Scotia',
            'PreferredLanguage': 'English',
            'Contact': contact_email,
            'Telephone': telephone,
            'Url': response.url
        }
