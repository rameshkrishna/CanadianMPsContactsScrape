import scrapy
from scrapy.spiders import Spider


class AlbertaSpider(Spider):
    """
    Spider to crawl and extract information about members from the Alberta National Assembly website.

    Attributes:
        name (str): The name of the spider.
        allowed_domains (list): A list of allowed domains for the spider.
        start_urls (list): A list of URLs where the spider will start crawling.
    """
    name = "Alberta"
    allowed_domains = ["assembly.ab.ca"]
    start_urls = [
        "https://www.assembly.ab.ca/members/members-of-the-legislative-assembly"]

    def parse(self, response):
        """
        The default callback used by Scrapy to process downloaded responses.

        This method is called when the spider has downloaded a page.
        It extracts links to individual member pages and follows them.

        Args:
            response (scrapy.http.Response): The response object containing the downloaded page content.
        """
        # Extract links to individual member pages
        mpp_index_links = response.css('div#mla-table a::attr(href) ').getall()
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
        name = response.css('h2 ::text').get().strip(
        ) if response.css('h2 ::text').get() else ''
        political_affiliation = response.css(
            'div.col-lg-6.my-3.px-3.px-lg-0 > p:nth-child(3)::text').get()
        constituency = response.css(
            'div.col-lg-6.my-3.px-3.px-lg-0 > p:nth-child(4)::text').get()
        contact_email = response.css(
            '#mla-header > div > div.card-body.bg-white.mla-contact > div.row.border-bottom.pt-2.ml-0.mr-0 > div.col-lg-auto.pb-2 > a:nth-child(6)::text').get()
        if not contact_email:
            contact_email = response.css(
                '#mla-header > div > div.card-body.bg-white.mla-contact > div.row.border-bottom.pt-2.ml-0.mr-0 > div.col-lg-auto.pb-2 > a:nth-child(10)::text').get()

        # will fix later not working for every page
        telephone = response.css(
            '#mla-header > div > div.card-body.bg-white.mla-contact > div.row.border-bottom.pt-2.ml-0.mr-0 > div.col-lg-auto.pb-2 > a:nth-child(3)::text').get()

        yield {
            'Name': name,
            'PoliticalAffiliation': political_affiliation,
            'Constituency': constituency,
            'ProvinceTerritory': 'Alberta',
            'PreferredLanguage': 'English',
            'Contact': contact_email,
            'Telephone': telephone,
            'Url': response.url
        }
