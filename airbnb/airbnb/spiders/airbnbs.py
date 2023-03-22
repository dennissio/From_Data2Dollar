import scrapy
from selenium import webdriver
import numpy as np
from scrapy.selector import Selector
from selenium.webdriver.support.select import Select
from time import sleep

#from scrapy_splash import SplashRequest
from scrapy.exceptions import CloseSpider
#from airbnb_scraper.items import AirbnbScraperItem

class AirbnbsSpider(scrapy.Spider):
    name = 'airbnbs'
    allowed_domains = ['airbnb.com']
    start_urls = ['https://www.airbnb.ch']
    custom_settings = {
    'ROBOTSTXT_OBEY': False
    }
    #def start_requests(self):
    city = 'Basel'
    person = '2'
    start_date = '2023-03-22'
    end_date = '2023-03-24'
    # Creating urls from cities
    #url = [f'https://www.airbnb.ch/s/{city}/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&price_filter_input_type=0&price_filter_num_nights=5&channel=EXPLORE&date_picker_type=calendar&checkin={start_date}&checkout={end_date}&adults={person}&source=structured_search_input_header&search_type=filter_change'] #[f'https://www.airbnb.com/s/{city}/homes/' for city in cities]
    # Launching crawling process for each city
        

    def parse(self, response):
        # Getting the hotels list of the page and iterating over each of them
        #soup = BeautifulSoup(response.text, features="lxml")
        #content = response.xpath('//*[@class = "cy5jw6o dir dir-ltr"]/text()').getall()
        #print(content)
        url = 'https://www.airbnb.ch/s/basel/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&price_filter_input_type=0&price_filter_num_nights=5&channel=EXPLORE&date_picker_type=calendar&checkin=2023-03-22&checkout=2023-03-24&adults=2&source=structured_search_input_header&search_type=filter_change' #[f'https://www.airbnb.com/s/{city}/homes/' for city in cities]
        self.driver = webdriver.Chrome('/Users/denizharimci/Driver/chromedriver_mac_arm64/chromedriver')
        self.driver.get(url)
        sleep(25)
        #self.driver.find_elements_by_xpath('//*[@class = "l1j9v1wn bmx2gr4 c1ih3c6 f1hzc007 dir dir-ltr"]/button').click()
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight - 10);")
        paginator = 0
        sel_page = Selector(text=self.driver.page_source)
        page = sel_page.xpath('//nav/div[@class= "_jro6t0"]/a/text()').extract()
        page = [int(x) for x in page]
        max_page = max(page)
        while paginator <= max_page:
            sleep(25)
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight - 10);")
            sel = Selector(text=self.driver.page_source)
            alle_zimmer = sel.xpath('//*[@class="c4mnd7m dir dir-ltr"]')
            
            for zimmer in alle_zimmer:
                title = zimmer.xpath('.//*[@class = "t1jojoys dir dir-ltr"]/text()').extract()
                anbieter = zimmer.xpath('.//div[@class= "f15liw5s s1cjsi4j dir dir-ltr"]/span/text()').extract()
                try:
                    anbieter = anbieter[1]
                except:
                    anbieter = "NA"
                preis = zimmer.xpath('.//*[@class = "_tt122m"]/span/text()').extract()
                rating = zimmer.xpath('.//span[@class = "r1dxllyb dir dir-ltr"]/text()').extract()
                yield {'title':title,
                'price':preis,
                'rating':rating,
                'provider':anbieter}
            sel = Selector(text=self.driver.page_source)
            sleep(5)
            weiter = self.driver.find_element_by_xpath('//*[@class="_1bfat5l l1j9v1wn dir dir-ltr"]')
            paginator = paginator + 1
            self.driver.execute_script("arguments[0].click();", weiter)
        self.driver.close()

       