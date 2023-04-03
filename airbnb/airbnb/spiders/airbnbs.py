import scrapy
from selenium import webdriver
import numpy as np
from scrapy.selector import Selector
from selenium.webdriver.support.select import Select
from time import sleep
from datetime import date
from selenium.webdriver.chrome.options import Options


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
    #global CHROME_PATH
    CHROME_PATH = '/Applications/Google Chrome.app'
    #global CHROMEDRIVER_PATH 
    CHROMEDRIVER_PATH = '/Users/denizharimci/Driver/chromedriver_mac_arm64/chromedriver'
    #global WINDOW_SIZE 
    WINDOW_SIZE = "1200,400"
    chrome_options = Options()
    chrome_options.binary_location = CHROME_PATH
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
    #def start_requests(self):
    
    # Creating urls from cities
    # url = [f'https://www.airbnb.ch/s/{city}/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&price_filter_input_type=0&price_filter_num_nights=5&channel=EXPLORE&date_picker_type=calendar&checkin={start_date}&checkout={end_date}&adults={person}&source=structured_search_input_header&search_type=filter_change'] #[f'https://www.airbnb.com/s/{city}/homes/' for city in cities]
    # Launching crawling process for each city

    def parse(self, response):
        #global CHROME_PATH
        CHROME_PATH = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
        #global CHROMEDRIVER_PATH 
        CHROMEDRIVER_PATH = '/Users/denizharimci/Driver/chromedriver_mac_arm64/chromedriver'
        #global WINDOW_SIZE 
        WINDOW_SIZE = "1200,400"
        chrome_options = Options()
        chrome_options.binary_location = CHROME_PATH
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
        # Getting the hotels list of the page and iterating over each of them
        datum = date.today()
        self.driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH,
                              chrome_options=chrome_options
                             )
        #self.driver = webdriver.Chrome('/Users/denizharimci/Driver/chromedriver_mac_arm64/chromedriver')
        
        dictionary = {'palma_e': ['La Palma', '2023-05-20', '2023-05-21', 'ja'], 'palma_n': ['La Palma', '2023-06-10', '2023-06-11', 'nein'], 'barca_e': ['Barcalona', '2023-05-28', '2023-05-29', 'ja'], 'barca_n': ['Barcalona', '2023-06-18', '2023-06-19', 'nein'], 'lyon_e': ['Lyon', '2023-05-20', '2023-05-21', 'ja'], 'lyon_n': ['Lyon', '2023-06-10', '2023-06-11', 'nein'], 
                      'bruessel_e': ['Bruessel', '2023-05-27', '2023-05-28', 'ja'], 'bruessel_n': ['Bruessel', '2023-06-17', '2023-06-18', 'nein'], 'muenchen_e': ['Muenchen', '2023-04-28', '2023-04-29', 'ja'], 'muenchen_n': ['Muenchen', '2023-05-18', '2023-05-19', 'nein'],
                       'adam_e': ['Amsterdam', '2023-04-27', '2023-04-28', 'ja'], 'adam_n': ['Amsterdam', '2023-05-18', '2023-05-19', 'nein'], 'sevilla_e': ['Sevilla', '2023-04-21', '2023-04-22', 'ja'], 'sevilla_n': ['Sevilla', '2023-05-12', '2023-05-13', 'nein'],
                        'helsinki_e': ['Helsinki', '2023-04-22', '2023-04-23', 'ja'], 'helsinki_n': ['Helsinki', '2023-05-13', '2023-05-14', 'nein'], 'brighton_e': ['Brighton', '2023-04-29', '2023-04-30', 'ja'], 'brighton_n': ['Brighton', '2023-05-20', '2023-05-21', 'nein'],
                        'hamburg_e': ['Hamburg', '2023-05-05', '2023-05-06', 'ja'], 'hamburg_n': ['Hamburg', '2023-05-26', '2023-05-27', 'nein'], 'berlin_e': ['Berlin', '2023-05-27', '2023-05-28', 'ja'], 'berlin_n': ['Berlin', '2023-06-17', '2023-06-18', 'nein'],
                        'monaco_e': ['Monaco-City', '2023-05-27', '2023-05-28', 'ja'], 'monaco_n': ['Monaco-City', '2023-06-17', '2023-06-18', 'nein'], 'nord_e': ['Noordwijk', '2023-04-21', '2023-04-22', 'ja'], 'nord_n': ['Noordwijk', '2023-05-12', '2023-05-13', 'nein'],
                        'bologna_e': ['Bologna', '2023-05-20', '2023-05-21', 'ja'], 'bologna_n': ['Bologna', '2023-06-10', '2023-06-11', 'nein'], 'halle_e': ['Halle', '2023-06-02', '2023-06-03', 'ja'], 'halle_n': ['Halle', '2023-06-23', '2023-06-24', 'nein']}          
        
        
        person = '2'
        #urls = 'https://www.airbnb.ch/s/basel/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&price_filter_input_type=0&price_filter_num_nights=5&channel=EXPLORE&date_picker_type=calendar&checkin=2023-03-27&checkout=2023-03-28&adults=2&source=structured_search_input_header&search_type=filter_change' #[f'https://www.airbnb.com/s/{city}/homes/' for city in cities]
        for destination in dictionary.keys():
            infos = dictionary[destination]
            city, start_date, end_date, event = infos[0], infos[1], infos[2], infos[3]
            url = 'https://www.airbnb.ch/s/{}/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&price_filter_input_type=0&price_filter_num_nights=5&channel=EXPLORE&date_picker_type=calendar&checkin={}&checkout={}&adults={}&source=structured_search_input_header&search_type=filter_change'.format(city, start_date, end_date, person) #[f'https://www.airbnb.com/s/{city}/homes/' for city in cities]
            self.driver.get(url)
            sleep(25)
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            paginator = 0
            sel_page = Selector(text=self.driver.page_source)
            page = sel_page.xpath('//nav/div[@class= "p1j2gy66 dir dir-ltr"]/a/text()').extract()
            pages = [int(x) for x in page]
            max_page = max(pages)
            while paginator <= max_page:
                sleep(25)
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                sel = Selector(text=self.driver.page_source)
                alle_zimmer = sel.xpath('//*[@class="c4mnd7m dir dir-ltr"]')
                for zimmer in alle_zimmer:
                    link = zimmer.xpath('.//*/div/a/@aria-labelledby').extract()
                    title = zimmer.xpath('.//*[@class = "t1jojoys dir dir-ltr"]/text()').extract()
                    anbieter = zimmer.xpath('.//*/div[@class= "f15liw5s s1cjsi4j dir dir-ltr"]/span/span/text()').getall()
                    try:
                        anbieter = anbieter[1]
                    except:
                        anbieter = "NA"
                    preis = zimmer.xpath('.//span[@class="_tyxjp1"]/text()').extract()
                    rating = zimmer.xpath('.//span[@class = "r1dxllyb dir dir-ltr"]/text()').extract()
                    yield {'date_crawl': datum, 'link': link,'title':title,
                    'price':preis,
                    'rating':rating,
                    'provider':anbieter, 'ort': city, 'start_buch': start_date, 'end_buch': end_date, 'event': event}
                sel = Selector(text=self.driver.page_source)
                sleep(5)
                weiter = self.driver.find_element_by_xpath('//*[@class="l1j9v1wn c1ytbx3a dir dir-ltr"]')
                paginator = paginator + 1
                self.driver.execute_script("arguments[0].click();", weiter)
        self.driver.close()

       