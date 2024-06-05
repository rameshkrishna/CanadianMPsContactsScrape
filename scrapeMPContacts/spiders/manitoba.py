import scrapy
from scrapy.spiders import Spider


class ManitobaSpider(Spider):
    """
    Spider to crawl and extract information about members from the Manitoba National Assembly website.

    Attributes:
        name (str): The name of the spider.
        allowed_domains (list): A list of allowed domains for the spider.
        start_urls (list): A list of URLs where the spider will start crawling.
    """
    name = "Manitoba"
    allowed_domains = ["gov.mb.ca"]
    start_urls = [
        "https://www.gov.mb.ca/legislature/members/mla_list_alphabetical.html"]

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
        name = response.css('h2::text').getall()[0].strip() if len(
            response.css('h2::text').getall()) > 1 else response.css('h2 a::text').get()
        political_affiliation = response.css('h3::text').get(
        ).strip() if response.css('h3::text').get() else ''
        constituency = response.css('h2::text').getall()[1].strip() if len(
            response.css('h2::text').getall()) > 1 else ''
        contact_email = response.css('a[href^="mailto:"]::text').get()

        # telephone = response.css('div.view-content.col-md ::text').getall()[8].strip()
        telephone = response.css(
            'h3:contains("Constituency Office:") + p ::text').re_first(r'Phone:\s*(\(\d{3}\) \d{3}-\d{4})')

        yield {
            'Name': name,
            'Govt': 'Provincial Leader',
            'PoliticalAffiliation': political_affiliation,
            'Constituency': constituency,
            'ProvinceTerritory': 'Manitoba',
            'PreferredLanguage': 'English',
            'Contact': contact_email,
            'Telephone': telephone,
            'Url': response.url
        }
