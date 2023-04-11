import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import pygsheets
from datetime import date
date = str(date.today().isoformat())

class VolSpider(CrawlSpider):
    name = 'vol'
    allowed_domains = ['dfes.vol.org.au']
    start_urls = ['https://dfes.vol.org.au/search']

    rules = (
        Rule(LinkExtractor(restrict_css=".stretched-link"), callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_css=".page-link"))
    )

    def parse_item(self, response):
        # Authorise the Google Sheet connection and open sheet
        gc = pygsheets.authorize(
            client_secret='client_secret_365419754254-ihnmrlocr9f4rurb6drb4ma576dc4ev0.apps.googleusercontent.com.json')
        wk1 = gc.open('DFES // Volunteer Opportunities').sheet1

        id = response.request.url[40:]
        name = response.css('.text-primary::text').get()
        organisation = response.css('.justify-content-between .font-weight-normal::text').get()
        time = response.css('#collapseOne li:nth-child(4) p::text').get()
        service = response.css('#collapseOne .mb-4 li::text').get()
        location = response.css('#collapseOne li:nth-child(1) p::text').get()[:-3]
        commitment = response.css('#collapseOne li:nth-child(3) p::text').get()
        url = response.request.url

        # print(location)

        new_opp = [date, id, name, organisation, location, service, commitment, time, url]
        exists = str(wk1.find(id))

        if id in exists:
            print("SKIP " + id + " ALREADY EXISTS")
        else:
            cells = wk1.get_all_values(include_tailing_empty_rows=False, include_tailing_empty=False,
                                       returnas='matrix')
            last_row = len(cells)
            wk1.insert_rows(last_row, number=1, values=new_opp)
