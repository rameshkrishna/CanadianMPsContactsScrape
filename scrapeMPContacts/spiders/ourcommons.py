import scrapy

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider

class OurcommonsSpider(scrapy.Spider):
    name = "ourcommons"
    allowed_domains = ["ourcommons.ca"]
    start_urls = ["https://www.ourcommons.ca/members/en/search"]
    rules = [
        Rule(
            LinkExtractor(
                canonicalize=True,
                unique=True,
                allow_domains= allowed_domains,
            ),
            follow=True,
            #process_links='link_filtering',
            callback="parse"
        ),]
    def parse(self, response):
    #   if not response.url.contains('members'):
    #      return
        author_page_links = response.css("a.ce-mip-mp-tile")
        yield from response.follow_all(author_page_links, self.parse_author)
    def parse_author(self,response):
        #print(response.url)
        yield {
            'Name':response.css('h1::text').get(),
            'Political Affiliation':response.css('dd.mip-mp-profile-caucus::text').get(),
            'Constituency': response.css('dd a::text').get(),
            'Province/Territory':response.css('dt:contains("Province / Territory:") + dd::text').get(),
            'Preferred_Language':response.css('dt:contains("Preferred Language:") + dd::text').get(),
            'Contact':response.css('#contact a::text').get(),
            'Telephone':response.css('p:contains("Telephone")::text').re_first(r'Telephone:\s+([\d-]+)'),
            'Url': response.url
        }