# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
# Zusaetzlich zu Scrapy importieren wir noch Selenium und die Systemtime
from selenium import webdriver
from time import sleep
import re
from datetime import date



# Dies ist unser normales von Scrapy angelegte Basistemplate 
class GetdataSpider(scrapy.Spider):
    name = 'getdata2'
    allowed_domains = ['www.booking.com']
    start_urls = ['https://www.booking.com/searchresults.de.html?ss=La+Palma%2C+Spanien&ssne=Manchester&ssne_untouched=Manchester&label=gen173nr-1FCAEoggI46AdIB1gEaCyIAQGYAQe4ARfIAQzYAQHoAQH4AQKIAgGoAgO4Avih-6AGwAIB0gIkYzBlODExNDktZTk3YS00YjIzLWFkOTktY2Y1ODMxMDRkOTEz2AIF4AIB&aid=304142&lang=de&sb=1&src_elem=sb&src=searchresults&dest_id=1405&dest_type=region&ac_position=1&ac_click_type=b&ac_langcode=de&ac_suggestion_list_length=5&search_selected=true&search_pageview_id=ac0f6e22242c0508&ac_meta=GhBhYzBmNmUyMjI0MmMwNTA4IAEoATICZGU6B2xhIHBsbWFAAEoAUAA%3D&checkin=2023-05-20&checkout=2023-05-21&group_adults=2&no_rooms=1&group_children=0&sb_travel_purpose=leisure']


    

    

    def parse(self, response):

        URL_Liste = [
            
            ('https://www.booking.com/searchresults.de.html?ss=Palma+de+Mallorca&ssne=Palma+de+Mallorca&ssne_untouched=Palma+de+Mallorca&label=gen173nr-1FCAEoggI46AdIB1gEaCyIAQGYAQe4ARfIAQzYAQHoAQH4AQKIAgGoAgO4Avih-6AGwAIB0gIkYzBlODExNDktZTk3YS00YjIzLWFkOTktY2Y1ODMxMDRkOTEz2AIF4AIB&aid=304142&lang=de&sb=1&src_elem=sb&src=searchresults&dest_id=-395224&dest_type=city&checkin=2023-05-20&checkout=2023-05-21&group_adults=2&no_rooms=1&group_children=0&sb_travel_purpose=leisure', 'La Palma', '2023-05-20', 'Ja'),
            ('https://www.booking.com/searchresults.de.html?ss=Palma+de+Mallorca&ssne=Palma+de+Mallorca&ssne_untouched=Palma+de+Mallorca&label=gen173nr-1FCAEoggI46AdIB1gEaCyIAQGYAQe4ARfIAQzYAQHoAQH4AQKIAgGoAgO4Avih-6AGwAIB0gIkYzBlODExNDktZTk3YS00YjIzLWFkOTktY2Y1ODMxMDRkOTEz2AIF4AIB&aid=304142&lang=de&sb=1&src_elem=sb&src=searchresults&dest_id=-395224&dest_type=city&checkin=2023-06-10&checkout=2023-06-11&group_adults=2&no_rooms=1&group_children=0&sb_travel_purpose=leisure', 'La Palma', '2023-06-01', 'Nein'),
            ('https://www.booking.com/searchresults.de.html?ss=Barcelona&ssne=Barcelona&ssne_untouched=Barcelona&label=gen173nr-1FCAEoggI46AdIB1gEaCyIAQGYAQe4ARfIAQzYAQHoAQH4AQKIAgGoAgO4Avih-6AGwAIB0gIkYzBlODExNDktZTk3YS00YjIzLWFkOTktY2Y1ODMxMDRkOTEz2AIF4AIB&aid=304142&lang=de&sb=1&src_elem=sb&src=searchresults&dest_id=-372490&dest_type=city&checkin=2023-05-28&checkout=2023-05-29&group_adults=2&no_rooms=1&group_children=0&sb_travel_purpose=leisure', 'Barcelona', '2023-05-28', 'Ja'),
            ('https://www.booking.com/searchresults.de.html?ss=Barcelona&ssne=Barcelona&ssne_untouched=Barcelona&highlighted_hotels=268664&label=New_German_DE_CH_20153967025-ZtI30A5vEwvl21bjygYpBwS640874806459%3Apl%3Ata%3Ap1%3Ap2%3Aac%3Aap%3Aneg&aid=318615&lang=de&sb=1&src_elem=sb&src=searchresults&dest_id=-372490&dest_type=city&checkin=2023-06-18&checkout=2023-06-19&group_adults=2&no_rooms=1&group_children=0&sb_travel_purpose=leisure','Barcelona','2023-06-18','Nein'),
            ('https://www.booking.com/searchresults.de.html?ss=lyon&efdco=1&label=gen173nr-1BCAEoggI46AdIM1gEaCyIAQGYAQe4ARfIAQzYAQHoAQGIAgGoAgO4AuP5kaEGwAIB0gIkYTVhMjBlNzctYTE4MC00YTgyLWE4YzYtYTk3YWYyZWM3MzZk2AIF4AIB&sid=e5adcbe6370a0533b7165ac64169e724&aid=304142&lang=de&sb=1&src_elem=sb&src=index&dest_id=-1448468&dest_type=city&ac_position=0&ac_click_type=b&ac_langcode=de&ac_suggestion_list_length=5&search_selected=true&search_pageview_id=bbff7eb1a127038d&ac_meta=GhBiYmZmN2ViMWExMjcwMzhkIAAoATICZGU6BGx5b25AAEoAUAA%3D&checkin=2023-05-20&checkout=2023-05-21&group_adults=2&no_rooms=1&group_children=0&sb_travel_purpose=leisure','Lyon','2023-05-20','Ja'),
            ('https://www.booking.com/searchresults.de.html?ss=Lyon&ssne=Lyon&ssne_untouched=Lyon&label=gen173nr-1BCAEoggI46AdIM1gEaCyIAQGYAQe4ARfIAQzYAQHoAQGIAgGoAgO4AuP5kaEGwAIB0gIkYTVhMjBlNzctYTE4MC00YTgyLWE4YzYtYTk3YWYyZWM3MzZk2AIF4AIB&sid=e5adcbe6370a0533b7165ac64169e724&aid=304142&lang=de&sb=1&src_elem=sb&src=searchresults&dest_id=-1448468&dest_type=city&checkin=2023-06-10&checkout=2023-06-11&group_adults=2&no_rooms=1&group_children=0&sb_travel_purpose=leisure','Lyon','2013-05-10','Nein'),
            ('https://www.booking.com/searchresults.de.html?ss=br%C3%BCssel&efdco=1&label=gen173nr-1BCAEoggI46AdIM1gEaCyIAQGYAQe4ARfIAQzYAQHoAQGIAgGoAgO4AuP5kaEGwAIB0gIkYTVhMjBlNzctYTE4MC00YTgyLWE4YzYtYTk3YWYyZWM3MzZk2AIF4AIB&sid=e5adcbe6370a0533b7165ac64169e724&aid=304142&lang=de&sb=1&src_elem=sb&src=index&dest_id=-1955538&dest_type=city&ac_position=0&ac_click_type=b&ac_langcode=de&ac_suggestion_list_length=5&search_selected=true&search_pageview_id=54bb7ef4252200d4&ac_meta=GhA1NGJiN2VmNDI1MjIwMGQ0IAAoATICZGU6CGJyw7xzc2VsQABKAFAA&checkin=2023-05-27&checkout=2023-05-28&group_adults=2&no_rooms=1&group_children=0&sb_travel_purpose=leisure','Brüssel','2023-05-27','Ja'),
            ('https://www.booking.com/searchresults.de.html?ss=Br%C3%BCssel&ssne=Br%C3%BCssel&ssne_untouched=Br%C3%BCssel&label=gen173nr-1BCAEoggI46AdIM1gEaCyIAQGYAQe4ARfIAQzYAQHoAQGIAgGoAgO4AuP5kaEGwAIB0gIkYTVhMjBlNzctYTE4MC00YTgyLWE4YzYtYTk3YWYyZWM3MzZk2AIF4AIB&sid=e5adcbe6370a0533b7165ac64169e724&aid=304142&lang=de&sb=1&src_elem=sb&src=searchresults&dest_id=-1955538&dest_type=city&checkin=2023-06-17&checkout=2023-06-18&group_adults=2&no_rooms=1&group_children=0&sb_travel_purpose=leisure','Brüssel','2023-06-17','Nein'),
            ('https://www.booking.com/searchresults.de.html?ss=M%C3%BCnchen&efdco=1&label=gen173nr-1BCAEoggI46AdIM1gEaCyIAQGYAQe4ARfIAQzYAQHoAQGIAgGoAgO4AuP5kaEGwAIB0gIkYTVhMjBlNzctYTE4MC00YTgyLWE4YzYtYTk3YWYyZWM3MzZk2AIF4AIB&sid=e5adcbe6370a0533b7165ac64169e724&aid=304142&lang=de&sb=1&src_elem=sb&src=index&dest_id=-1829149&dest_type=city&ac_position=0&ac_click_type=b&ac_langcode=de&ac_suggestion_list_length=5&search_selected=true&search_pageview_id=60e37f2e647f0223&ac_meta=GhA2MGUzN2YyZTY0N2YwMjIzIAAoATICZGU6CE3DvG5jaGVuQABKAFAA&checkin=2023-04-28&checkout=2023-04-29&group_adults=2&no_rooms=1&group_children=0&sb_travel_purpose=leisure','München','2023-04-28','Ja'),
            ('https://www.booking.com/searchresults.de.html?ss=M%C3%BCnchen&ssne=M%C3%BCnchen&ssne_untouched=M%C3%BCnchen&label=gen173nr-1BCAEoggI46AdIM1gEaCyIAQGYAQe4ARfIAQzYAQHoAQGIAgGoAgO4AuP5kaEGwAIB0gIkYTVhMjBlNzctYTE4MC00YTgyLWE4YzYtYTk3YWYyZWM3MzZk2AIF4AIB&sid=e5adcbe6370a0533b7165ac64169e724&aid=304142&lang=de&sb=1&src_elem=sb&src=searchresults&dest_id=-1829149&dest_type=city&checkin=2023-05-19&checkout=2023-05-20&group_adults=2&no_rooms=1&group_children=0&sb_travel_purpose=leisure','München','2023-05-19','Nein'),
            ('https://www.booking.com/searchresults.de.html?ss=amsterdam&efdco=1&label=gen173nr-1BCAEoggI46AdIM1gEaCyIAQGYAQe4ARfIAQzYAQHoAQGIAgGoAgO4AuP5kaEGwAIB0gIkYTVhMjBlNzctYTE4MC00YTgyLWE4YzYtYTk3YWYyZWM3MzZk2AIF4AIB&sid=e5adcbe6370a0533b7165ac64169e724&aid=304142&lang=de&sb=1&src_elem=sb&src=index&dest_id=145&dest_type=district&ac_position=0&ac_click_type=b&ac_langcode=de&ac_suggestion_list_length=5&search_selected=true&search_pageview_id=bf327f7f937602d4&ac_meta=GhBiZjMyN2Y3ZjkzNzYwMmQ0IAAoATICZGU6CWFtc3RlcmRhbUAASgBQAA%3D%3D&checkin=2023-04-27&checkout=2023-04-28&group_adults=2&no_rooms=1&group_children=0&sb_travel_purpose=leisure','Amsterdam','2023-04-27','Ja'),
            ('https://www.booking.com/searchresults.de.html?ss=Stadtzentrum+von+Amsterdam&ssne=Stadtzentrum+von+Amsterdam&ssne_untouched=Stadtzentrum+von+Amsterdam&label=gen173nr-1BCAEoggI46AdIM1gEaCyIAQGYAQe4ARfIAQzYAQHoAQGIAgGoAgO4AuP5kaEGwAIB0gIkYTVhMjBlNzctYTE4MC00YTgyLWE4YzYtYTk3YWYyZWM3MzZk2AIF4AIB&sid=e5adcbe6370a0533b7165ac64169e724&aid=304142&lang=de&sb=1&src_elem=sb&src=searchresults&dest_id=145&dest_type=district&checkin=2023-05-18&checkout=2023-05-19&group_adults=2&no_rooms=1&group_children=0&sb_travel_purpose=leisure','Amsterdam','2023-05-18','Nein'),
            ('https://www.booking.com/searchresults.de.html?ss=Sevilla&ssne=Sevilla&ssne_untouched=Sevilla&label=gen173nr-1BCAEoggI46AdIM1gEaCyIAQGYAQe4ARfIAQzYAQHoAQGIAgGoAgO4AuP5kaEGwAIB0gIkYTVhMjBlNzctYTE4MC00YTgyLWE4YzYtYTk3YWYyZWM3MzZk2AIF4AIB&sid=e5adcbe6370a0533b7165ac64169e724&aid=304142&lang=de&sb=1&src_elem=sb&src=searchresults&dest_id=-402849&dest_type=city&checkin=2023-04-21&checkout=2023-04-22&group_adults=2&no_rooms=1&group_children=0&sb_travel_purpose=leisure','Sevilla','2023-04-21','Ja'),
            ('https://www.booking.com/searchresults.de.html?ss=Sevilla&ssne=Sevilla&ssne_untouched=Sevilla&label=gen173nr-1BCAEoggI46AdIM1gEaCyIAQGYAQe4ARfIAQzYAQHoAQGIAgGoAgO4AuP5kaEGwAIB0gIkYTVhMjBlNzctYTE4MC00YTgyLWE4YzYtYTk3YWYyZWM3MzZk2AIF4AIB&sid=e5adcbe6370a0533b7165ac64169e724&aid=304142&lang=de&sb=1&src_elem=sb&src=searchresults&dest_id=-402849&dest_type=city&checkin=2023-05-12&checkout=2023-05-13&group_adults=2&no_rooms=1&group_children=0&sb_travel_purpose=leisure','Sevilla','2023-05-12','Nein'),
            ('https://www.booking.com/searchresults.de.html?ss=helsiki&efdco=1&label=gen173nr-1BCAEoggI46AdIM1gEaCyIAQGYAQe4ARfIAQzYAQHoAQGIAgGoAgO4AuP5kaEGwAIB0gIkYTVhMjBlNzctYTE4MC00YTgyLWE4YzYtYTk3YWYyZWM3MzZk2AIF4AIB&sid=e5adcbe6370a0533b7165ac64169e724&aid=304142&lang=de&sb=1&src_elem=sb&src=index&dest_id=-1364995&dest_type=city&ac_position=0&ac_click_type=b&ac_langcode=de&ac_suggestion_list_length=5&search_selected=true&search_pageview_id=54e28006e540008e&ac_meta=GhA1NGUyODAwNmU1NDAwMDhlIAAoATICZGU6B2hlbHNpa2lAAUoIaGVsc2lua2lQ7xY%3D&checkin=2023-04-22&checkout=2023-04-23&group_adults=2&no_rooms=1&group_children=0&sb_travel_purpose=leisure','Helsinki','2023-04-22','Ja'),
            ('https://www.booking.com/searchresults.de.html?ss=Helsinki&ssne=Helsinki&ssne_untouched=Helsinki&label=gen173nr-1BCAEoggI46AdIM1gEaCyIAQGYAQe4ARfIAQzYAQHoAQGIAgGoAgO4AuP5kaEGwAIB0gIkYTVhMjBlNzctYTE4MC00YTgyLWE4YzYtYTk3YWYyZWM3MzZk2AIF4AIB&sid=e5adcbe6370a0533b7165ac64169e724&aid=304142&lang=de&sb=1&src_elem=sb&src=searchresults&dest_id=-1364995&dest_type=city&checkin=2023-05-13&checkout=2023-05-14&group_adults=2&no_rooms=1&group_children=0&sb_travel_purpose=leisure','Helsinki','2023-05-13','Nein'),
            ('https://www.booking.com/searchresults.de.html?ss=Brighton+%26+Hove&ssne=Brighton+%26+Hove&ssne_untouched=Brighton+%26+Hove&label=gen173nr-1BCAEoggI46AdIM1gEaCyIAQGYAQe4ARfIAQzYAQHoAQGIAgGoAgO4AuP5kaEGwAIB0gIkYTVhMjBlNzctYTE4MC00YTgyLWE4YzYtYTk3YWYyZWM3MzZk2AIF4AIB&sid=e5adcbe6370a0533b7165ac64169e724&aid=304142&lang=de&sb=1&src_elem=sb&src=searchresults&dest_id=-2590884&dest_type=city&checkin=2023-04-29&checkout=2023-04-30&group_adults=2&no_rooms=1&group_children=0&sb_travel_purpose=leisure','Brighton','2023-04-29','Ja'),
            ('https://www.booking.com/searchresults.de.html?ss=Brighton+%26+Hove&ssne=Brighton+%26+Hove&ssne_untouched=Brighton+%26+Hove&label=gen173nr-1BCAEoggI46AdIM1gEaCyIAQGYAQe4ARfIAQzYAQHoAQGIAgGoAgO4AuP5kaEGwAIB0gIkYTVhMjBlNzctYTE4MC00YTgyLWE4YzYtYTk3YWYyZWM3MzZk2AIF4AIB&sid=e5adcbe6370a0533b7165ac64169e724&aid=304142&lang=de&sb=1&src_elem=sb&src=searchresults&dest_id=-2590884&dest_type=city&checkin=2023-05-20&checkout=2023-05-21&group_adults=2&no_rooms=1&group_children=0&sb_travel_purpose=leisure','Brighton','2023-05-20','Nein'),
            ('https://www.booking.com/searchresults.de.html?ss=Hamburg&ssne=Hamburg&ssne_untouched=Hamburg&label=gen173nr-1BCAEoggI46AdIM1gEaCyIAQGYAQe4ARfIAQzYAQHoAQGIAgGoAgO4AuP5kaEGwAIB0gIkYTVhMjBlNzctYTE4MC00YTgyLWE4YzYtYTk3YWYyZWM3MzZk2AIF4AIB&sid=e5adcbe6370a0533b7165ac64169e724&aid=304142&lang=de&sb=1&src_elem=sb&src=searchresults&dest_id=-1785434&dest_type=city&checkin=2023-05-05&checkout=2023-05-06&group_adults=2&no_rooms=1&group_children=0&sb_travel_purpose=leisure','Hamburg','2023-05-05','Ja'),
            ('https://www.booking.com/searchresults.de.html?ss=Hamburg&ssne=Hamburg&ssne_untouched=Hamburg&label=gen173nr-1BCAEoggI46AdIM1gEaCyIAQGYAQe4ARfIAQzYAQHoAQGIAgGoAgO4AuP5kaEGwAIB0gIkYTVhMjBlNzctYTE4MC00YTgyLWE4YzYtYTk3YWYyZWM3MzZk2AIF4AIB&sid=e5adcbe6370a0533b7165ac64169e724&aid=304142&lang=de&sb=1&src_elem=sb&src=searchresults&dest_id=-1785434&dest_type=city&checkin=2023-05-26&checkout=2023-05-27&group_adults=2&no_rooms=1&group_children=0&sb_travel_purpose=leisure','Hamburg','2023-05-26','Nein'),
            ('https://www.booking.com/searchresults.de.html?ss=Berlin%2C+Berlin+%28Bundesland%29%2C+Deutschland&ssne=Davos&ssne_untouched=Davos&label=de-vUBLmwTlH0dPnMMjqzPi3gS410502041971%3Apl%3Ata%3Ap1%3Ap22.563.000%3Aac%3Aap%3Aneg%3Afi%3Atikwd-65526620%3Alp1003113%3Ali%3Adec%3Adm%3Appccp%3DUmFuZG9tSVYkc2RlIyh9YYnX0UuDUyu9DO6pj_qLMMQ&sid=2541c6c221ef5f7a1c0e307e43c83562&aid=376364&lang=de&sb=1&src_elem=sb&src=searchresults&dest_id=-1746443&dest_type=city&ac_position=0&ac_click_type=b&ac_langcode=de&ac_suggestion_list_length=5&search_selected=true&search_pageview_id=eb1c7c5953210027&ac_meta=GhBlYjFjN2M1OTUzMjEwMDI3IAAoATICZGU6BmJlcmxpbkAASgBQAA%3D%3D&checkin=2023-05-27&checkout=2023-05-28&group_adults=2&no_rooms=1&group_children=0&sb_travel_purpose=leisure','Berlin','2023-05-27','Ja'),
            ('https://www.booking.com/searchresults.de.html?ss=Berlin&ssne=Berlin&ssne_untouched=Berlin&label=de-vUBLmwTlH0dPnMMjqzPi3gS410502041971%3Apl%3Ata%3Ap1%3Ap22.563.000%3Aac%3Aap%3Aneg%3Afi%3Atikwd-65526620%3Alp1003113%3Ali%3Adec%3Adm%3Appccp%3DUmFuZG9tSVYkc2RlIyh9YYnX0UuDUyu9DO6pj_qLMMQ&sid=2541c6c221ef5f7a1c0e307e43c83562&aid=376364&lang=de&sb=1&src_elem=sb&src=searchresults&dest_id=-1746443&dest_type=city&checkin=2023-06-17&checkout=2023-06-18&group_adults=2&no_rooms=1&group_children=0&sb_travel_purpose=leisure','Berlin','2023-06-17','Nein'),
            ('https://www.booking.com/searchresults.de.html?ss=Monaco&ssne=Davos&ssne_untouched=Davos&label=gen173nr-1BCAEoggI46AdIM1gEaCyIAQGYAQe4ARfIAQzYAQHoAQGIAgGoAgO4AuP5kaEGwAIB0gIkYTVhMjBlNzctYTE4MC00YTgyLWE4YzYtYTk3YWYyZWM3MzZk2AIF4AIB&sid=e5adcbe6370a0533b7165ac64169e724&aid=304142&lang=de&sb=1&src_elem=sb&src=searchresults&dest_id=140&dest_type=country&ac_position=1&ac_click_type=b&ac_langcode=de&ac_suggestion_list_length=5&search_selected=true&search_pageview_id=810580d7ea720275&ac_meta=GhA4MTA1ODBkN2VhNzIwMjc1IAEoATICZGU6Bm1vbmFjb0AASgBQAA%3D%3D&checkin=2023-05-27&checkout=2023-05-28&group_adults=2&no_rooms=1&group_children=0&sb_travel_purpose=leisure','Monaco','2023-05-27','Ja'),
            ('https://www.booking.com/searchresults.de.html?ss=Monaco&ssne=Monaco&ssne_untouched=Monaco&label=gen173nr-1BCAEoggI46AdIM1gEaCyIAQGYAQe4ARfIAQzYAQHoAQGIAgGoAgO4AuP5kaEGwAIB0gIkYTVhMjBlNzctYTE4MC00YTgyLWE4YzYtYTk3YWYyZWM3MzZk2AIF4AIB&sid=e5adcbe6370a0533b7165ac64169e724&aid=304142&lang=de&sb=1&src_elem=sb&src=searchresults&dest_id=140&dest_type=country&checkin=2023-06-17&checkout=2023-06-18&group_adults=2&no_rooms=1&group_children=0&sb_travel_purpose=leisure','Monaco','2023-06-17','Nein'),
            ('https://www.booking.com/searchresults.de.html?ss=Noordwijk&ssne=Noordwijk&ssne_untouched=Noordwijk&label=gen173nr-1BCAEoggI46AdIM1gEaCyIAQGYAQe4ARfIAQzYAQHoAQGIAgGoAgO4AuP5kaEGwAIB0gIkYTVhMjBlNzctYTE4MC00YTgyLWE4YzYtYTk3YWYyZWM3MzZk2AIF4AIB&sid=e5adcbe6370a0533b7165ac64169e724&aid=304142&lang=de&sb=1&src_elem=sb&src=searchresults&dest_id=-2150478&dest_type=city&checkin=2023-04-21&checkout=2023-04-22&group_adults=2&no_rooms=1&group_children=0&sb_travel_purpose=leisure','Noordwjik','2023-04-21','Ja'),
            ('https://www.booking.com/searchresults.de.html?ss=Noordwijk&ssne=Noordwijk&ssne_untouched=Noordwijk&label=gen173nr-1BCAEoggI46AdIM1gEaCyIAQGYAQe4ARfIAQzYAQHoAQGIAgGoAgO4AuP5kaEGwAIB0gIkYTVhMjBlNzctYTE4MC00YTgyLWE4YzYtYTk3YWYyZWM3MzZk2AIF4AIB&sid=e5adcbe6370a0533b7165ac64169e724&aid=304142&lang=de&sb=1&src_elem=sb&src=searchresults&dest_id=-2150478&dest_type=city&checkin=2023-05-12&checkout=2023-05-13&group_adults=2&no_rooms=1&group_children=0&sb_travel_purpose=leisure','Noordwjik','2023-05-12','Nein'),
            ('https://www.booking.com/searchresults.de.html?ss=Bologna&ssne=Bologna&ssne_untouched=Bologna&label=gen173nr-1BCAEoggI46AdIM1gEaCyIAQGYAQe4ARfIAQzYAQHoAQGIAgGoAgO4AuP5kaEGwAIB0gIkYTVhMjBlNzctYTE4MC00YTgyLWE4YzYtYTk3YWYyZWM3MzZk2AIF4AIB&sid=e5adcbe6370a0533b7165ac64169e724&aid=304142&lang=de&sb=1&src_elem=sb&src=searchresults&dest_id=-111742&dest_type=city&checkin=2023-05-20&checkout=2023-05-21&group_adults=2&no_rooms=1&group_children=0&sb_travel_purpose=leisure','Bologna','2023-05','Ja'),
            ('https://www.booking.com/searchresults.de.html?ss=Bologna&ssne=Bologna&ssne_untouched=Bologna&label=gen173nr-1BCAEoggI46AdIM1gEaCyIAQGYAQe4ARfIAQzYAQHoAQGIAgGoAgO4AuP5kaEGwAIB0gIkYTVhMjBlNzctYTE4MC00YTgyLWE4YzYtYTk3YWYyZWM3MzZk2AIF4AIB&sid=e5adcbe6370a0533b7165ac64169e724&aid=304142&lang=de&sb=1&src_elem=sb&src=searchresults&dest_id=-111742&dest_type=city&checkin=2023-06-10&checkout=2023-06-11&group_adults=2&no_rooms=1&group_children=0&sb_travel_purpose=leisure','Bologna','2023-06-10','Nein'),
            ('https://www.booking.com/searchresults.de.html?ss=Hallowell&ssne=Hallowell&ssne_untouched=Hallowell&label=gen173nr-1BCAEoggI46AdIM1gEaCyIAQGYAQe4ARfIAQzYAQHoAQGIAgGoAgO4AuP5kaEGwAIB0gIkYTVhMjBlNzctYTE4MC00YTgyLWE4YzYtYTk3YWYyZWM3MzZk2AIF4AIB&sid=e5adcbe6370a0533b7165ac64169e724&aid=304142&lang=de&sb=1&src_elem=sb&src=searchresults&dest_id=20052141&dest_type=city&checkin=2023-06-02&checkout=2023-06-03&group_adults=2&no_rooms=1&group_children=0&sb_travel_purpose=leisure','Halle','2023-06-02','Ja'),
            ('https://www.booking.com/searchresults.de.html?ss=Hallowell&ssne=Hallowell&ssne_untouched=Hallowell&label=gen173nr-1BCAEoggI46AdIM1gEaCyIAQGYAQe4ARfIAQzYAQHoAQGIAgGoAgO4AuP5kaEGwAIB0gIkYTVhMjBlNzctYTE4MC00YTgyLWE4YzYtYTk3YWYyZWM3MzZk2AIF4AIB&sid=e5adcbe6370a0533b7165ac64169e724&aid=304142&lang=de&sb=1&src_elem=sb&src=searchresults&dest_id=20052141&dest_type=city&checkin=2023-06-23&checkout=2023-06-24&group_adults=2&no_rooms=1&group_children=0&sb_travel_purpose=leisure','Halle','2023-06-23','Nein')]

        self.driver = webdriver.Chrome('C:\Drivers\chromedriver_win32\chromedriver.exe')
            
        for values in URL_Liste:
            # Hier integrieren wir den Webdriver
            url = values[0]
            stadt_name = values[1]
            datum_event = values[2]
            eventYN = values[3]
            
            self.driver.get(url)
            #Wir benoetigen eine while-Schleife, die ueberprueft, ob es noch eine naechste Seite gibt oder nicht
            a = 0
            while a==0:
                  
                sel = Selector(text=self.driver.page_source)
                single_etikette = sel.xpath('//*[@class="a826ba81c4 fe821aea6c fa2f36ad22 afd256fc79 d08f526e0d ed11e24d01 ef9845d4b3 da89aeb942"]')
                
                for etikette in single_etikette:
                    
                    datum_heute = date.today()
                    hotel_name = etikette.xpath('.//*[@class="fcab3ed991 a23c043802"]/text()').extract_first()
                    hotel_preis_raw = etikette.xpath('.//*[@class="fcab3ed991 fbd1d3018c e729ed5ab6"]/text()').extract_first()
                    hotel_bewertung = etikette.xpath('.//*[@class="b5cd09854e d10a6220b4"]/text()').extract_first()
                    hotel_link = etikette.xpath('.//h3[@class="a4225678b2"]/a/@href').extract_first()
                    hotel_anbieter = etikette.xpath('.//*[@class="d8eab2cf7f"]/text()').extract_first()

                    #extrahiert die Zahl aus den Rohdaten
                    hotel_preis = re.search(r'\d+', hotel_preis_raw).group()

                
                    #If funktion um zu prüfen ob di Unterkunft gewerblich oder privat angeboten wird
                    if hotel_anbieter == "Von einem privaten Gastgeber geführt":
                        anbieter_text = "privat"
                    else:
                        anbieter_text = "gewerblich"

                    yield { 'Stadt': stadt_name,
                        'Datum scraped': datum_heute,
                        'Name': f'"{hotel_name}"',
                        'Preis': hotel_preis,
                        'Event Ja/Nein': eventYN,
                        'Datum': datum_event,
                        'Bewertung': hotel_bewertung,
                        'Anbieter': anbieter_text,
                        'Link': hotel_link}


                # Da der "Naechste Seite" Button im Sichtfeld sein muss, scrollen wir auf der Webseite nach unten
                try: 
                    element = self.driver.find_element("xpath",' //button[@class="fc63351294 a822bdf511 e3c025e003 fa565176a8 f7db01295e c334e6f658 e1b7cfea84 f9d6150b8e"]')
                    self.driver.execute_script("arguments[0].scrollIntoView(0, document.documentElement.scrollHeight-5);", element)
                    sel = Selector(text=self.driver.page_source)
                    sleep(5)
                    self.driver.find_element("xpath",' //*[@class="f32a99c8d1 f78c3700d2"]/button[@class="fc63351294 a822bdf511 e3c025e003 fa565176a8 f7db01295e c334e6f658 e1b7cfea84 f9d6150b8e"]').click()
                except: a = 1
                
                
                sleep(5)
        # Am Ende schliessen wir den Webdriver
        self.driver.close()
