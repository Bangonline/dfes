import scrapy
import pygsheets
from datetime import date
date = str(date.today().isoformat())
class dfesvolunteerspider(scrapy.Spider):
    name = 'dfesvolunteer'
    start_urls = ['https://dfes.vol.org.au/search']
    def parse(self, response):
        # Authorise the Google Sheet connection and open sheet
        gc = pygsheets.authorize(
            client_secret='client_secret_365419754254-ihnmrlocr9f4rurb6drb4ma576dc4ev0.apps.googleusercontent.com.json')
        wk1 = gc.open('DFES // Volunteer Opportunities').sheet1
        # opps = response.css('article.position-relative.border-bottom.border-gray-400.mb-4')
        #
        # for opp in opps:
        #     url = str("https://dfes.vol.org.au" + opp.css('a.stretched-link::attr(href)').get())
        #     print(url)
        for opportunities in response.css('article.position-relative.border-bottom.border-gray-400.mb-4'):
            # variables to scrape from DFES website
            name = response.css('.text-primary::text').get()
            organisation = response.css('.justify-content-between .font-weight-normal::text').get()
            time = response.css('#collapseOne li:nth-child(4) p::text').get()
            service = response.css('#collapseOne .mb-4 li::text').get()
            location = response.css('#collapseOne li:nth-child(1) p::text').get()
            commitment = response.css('#collapseOne li:nth-child(3) p::text').get()
            url = response.request.url
            # name = opportunities.css('a.stretched-link::text').get()
            # organisation = opportunities.css('h3.h4.font-weight-normal.mb-2::text').get()
            # location = opportunities.css('ul.list-inline').get()[
            #            opportunities.css('ul.list-inline').get().find("Location:</span>\n") + len(
            #                "Location:</span>\n"):opportunities.css('ul.list-inline').get().find("\n</li>\n</ul>")]
            # url = str("https://dfes.vol.org.au" + opportunities.css('a.stretched-link').attrib['href'])
            # description = opportunities.css('p').get()[
            #               opportunities.css('p').get().find("<p>") + len("<p>"):opportunities.css('p').get().find(
            #                   "</p>")]
            new_opp = [date, name, organisation, location, service, commitment, time, url]
            exists = str(wk1.find(url))
            # Variables from detail page
            # name = response.css('.text-primary::text').get()
            # organisation = response.css('.justify-content-between .font-weight-normal::text').get()
            # location = response.css('#collapseOne li:nth-child(1) p::text').get()
            # service = response.css('#collapseOne .mb-4 li::text').get()
            # commitment = response.css('#collapseOne li:nth-child(3) p::text').get()
            # time = response.css('#collapseOne li:nth-child(4) p::text').get()
            # url = response.css('a.stretched-link::attr(href)').get()
            # check if opportunity already exists in sheet using URL as unique identifier
            if url in exists:
                pass
            else:
                # if not, add new row to the end of the sheet with scraped variables
                cells = wk1.get_all_values(include_tailing_empty_rows=False, include_tailing_empty=False,
                                           returnas='matrix')
                last_row = len(cells)
                wk1.insert_rows(last_row, number=1, values=new_opp)
        next_page = "https://dfes.vol.org.au/search" + response.css('li.page-item.next').css('a.page-link').attrib[
            'href']
        # navigate to next page to scrape, end if no next page
        if next_page:
            yield response.follow(next_page, callback=self.parse)